import logging
import jwt

from fastapi import  APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session
from src.database import get_db

from src.general.auth.schema.login import UserLoginSchema
from src.general.auth.schema.profile import UserProfileSchema
from src.general.auth.schema.registration import UserRegistrationSchema
from src.general.auth.schema.access_token import AccessTokenSchema
from src.general.order.schema.user_order_detail import UserOrderDetailSchema
from src.general.order.service import OrderService

from src.helper.message.schema import MessageSchema
from src.helper.error.schema import ErrorSchema

from src.general.auth.service.auth import AuthService
from src.general.auth.service.user import UserService

from src.config import oauth2_scheme, SWAGGER_GROUPS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/user")


@user_router.post(
    "/register/",
    tags=[SWAGGER_GROUPS["user"]],
    response_model=MessageSchema,
    responses={
        200:{
            "model": MessageSchema
        },
        400:{
            "model": ErrorSchema
        },
        500:{
            "model": ErrorSchema
        }
    }
)
async def register(user_reg_sch: UserRegistrationSchema,
                   db: Session = Depends(get_db),
                   user_service: UserService = Depends(UserService),
                   ):
    try:
        user = await user_service.get_user_by_email(db,  user_reg_sch.email)

        if user:
            logger.warning(f"(Registration) User already register: {user_reg_sch.email}")
            raise HTTPException(status_code=400, detail="User already exist")

        user = await user_service.create_user(db, user_reg_sch.name, user_reg_sch.tel, user_reg_sch.email, user_reg_sch.password)

        logger.info(f"(Registration) User successful register {user.id}")
        return MessageSchema(messageDigest=str(user.id),
                             description="User registered successfully"
                             )
    except HTTPException:
        raise
    except ValueError as validation_error:
        logger.warning(f"(Registration) Validation error: {validation_error}")
        raise HTTPException(status_code=400, detail=str(validation_error))
    except Exception as e:
        logger.error(f"(Registration) Error {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.post(
    "/login/",
    tags=[SWAGGER_GROUPS["user"]],
    response_model=AccessTokenSchema,
    responses={
        200:{
            "model": AccessTokenSchema
        },
        400:{
            "model": ErrorSchema
        },
        500:{
            "model": ErrorSchema
        }
    }
)
async def login(user_log_sch: UserLoginSchema,
                   db: Session = Depends(get_db),
                   user_service: UserService = Depends(UserService),
                   auth_service: AuthService = Depends(AuthService),
                   ):
    try:
        if not await user_service.verify_password(db, user_log_sch.email, user_log_sch.password):
            logger.warning(f"(Login) Failed login for user with email: {user_log_sch.email}")
            raise HTTPException(status_code=400, detail="Invalid credentials")

        user = await user_service.get_user_by_email(db,  user_log_sch.email)

        access_token = await auth_service.create_access_token(
            data={"sub": str(user.id)}
        )

        logger.info(f"(Login) Login successful for user with ID: {user.id}")
        return AccessTokenSchema(access_token=access_token)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Registration) Error {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.get(
    "/{user_id}/orders",
    tags=[SWAGGER_GROUPS["user"]],
    response_model=list[UserOrderDetailSchema],
    responses={
        200: {
            "model": list[UserOrderDetailSchema]
        },
        401: {
            "model": ErrorSchema
        },
        403: {
            "model": ErrorSchema
        },
        500: {
            "model": ErrorSchema
        },
    }
)
async def get_user_orders(user_id: int,
                          db: Session = Depends(get_db),
                          access_token: str = Depends(oauth2_scheme),
                          auth_service: AuthService = Depends(AuthService),
                          order_service: OrderService = Depends(OrderService)
                          ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get user orders) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        orders = await order_service.get_user_orders(db, user_id)

        if not orders:
            logger.info(f"(Get user orders) User's {user_id} orders not found:")
            raise HTTPException(status_code=404, detail="No orders found for this user")

        logger.info(f"(Get user orders) User's orders successful found")

        orders_schema = []

        for order in orders:
            orders_schema.append(
                UserOrderDetailSchema(
                    id=order.id,
                    driver_id=order.driver_id,
                    driver_class=order.driver_class,
                    car=order.car,
                    house_from_id=order.house_from_id,
                    house_from_street=order.house_from_street,
                    house_from_building=order.house_from_building,
                    house_from_number=order.house_from_number,
                    house_to_id=order.house_to_id,
                    house_to_street=order.house_to_street,
                    house_to_building=order.house_to_building,
                    house_to_number=order.house_to_number,
                    order_time=order.order_date
                )
            )

        return orders_schema

    except jwt.PyJWTError as e:
        logger.warning(f"(Get user orders) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get user orders) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.get(
    "/",
    tags=[SWAGGER_GROUPS["user"]],
    response_model=UserProfileSchema,
    responses={
        200:{
            "model": UserProfileSchema
        },
        401:{
            "model": ErrorSchema
        },
        403:{
            "model": ErrorSchema
        },
        500:{
            "model": ErrorSchema
        }
    }
)
async def get_profile(access_token: str = Depends(oauth2_scheme),
                      db: Session = Depends(get_db),
                      user_service: UserService = Depends(UserService),
                      auth_service: AuthService = Depends(AuthService)
                      ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get user profile) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)

        user = await user_service.get_user_by_id(db, token_data["sub"])

        logger.info(f"(Get user profile) Successful get profile with id: {user.id}")

        return UserProfileSchema(
            id=user.id,
            name=user.name,
            tel=user.tel,
            email=user.email
        )
    except jwt.PyJWTError as e:
        logger.warning(f"(Get user profile) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get user profile) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@user_router.put(
    "/",
    tags=[SWAGGER_GROUPS["user"]],
    response_model=UserProfileSchema,
    responses={
        200:{
            "model": UserProfileSchema
        },
        401:{
            "model": ErrorSchema
        },
        403:{
            "model": ErrorSchema
        },
        500:{
            "model": ErrorSchema
        }
    }
)
async def edit_profile(user_profile: UserProfileSchema,
                       access_token: str = Depends(oauth2_scheme),
                       db: Session = Depends(get_db),
                       user_service: UserService = Depends(UserService),
                       auth_service: AuthService = Depends(AuthService)
                       ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Update user profile) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)

        user_id = token_data["sub"]
        user = await user_service.get_user_by_id(db, user_id)

        updated_user = await user_service.update_user(
            db,
            _id=user.id,
            name=user_profile.name,
            tel=user_profile.tel,
            email=user_profile.email
        )

        logger.info(f"(Update user profile) Successfully updated profile with id: {updated_user.id}")

        return UserProfileSchema(
            id=user.id,
            name=updated_user.name,
            tel=updated_user.tel,
            email=updated_user.email
        )
    except jwt.PyJWTError as e:
        logger.warning(f"(Update user profile) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Update user profile) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@user_router.post(
    "/logout/",
    tags=[SWAGGER_GROUPS["user"]],
    response_model=MessageSchema,
    responses={
        200:{
            "model": MessageSchema
        },
        400:{
            "model": ErrorSchema
        },
        500:{
            "model": ErrorSchema
        }
    }
)
async def logout(access_token: str = Depends(oauth2_scheme),
                 db: Session = Depends(get_db),
                 auth_service: AuthService = Depends(AuthService),
                 ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Logout) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        await auth_service.revoke_access_token(db, access_token)

        logger.info(f"(Logout) Token was revoked now: {access_token}")

        return MessageSchema(description="Token was successfully revoked")
    except jwt.PyJWTError as e:
        logger.warning(f"(Logout) Bad token {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Logout) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")