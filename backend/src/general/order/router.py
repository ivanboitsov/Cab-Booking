import logging
import jwt
import random

from src.database import get_db
from sqlalchemy.orm import Session

from src.config import oauth2_scheme, SWAGGER_GROUPS
from fastapi import APIRouter, Depends, HTTPException

from src.general.auth.service.user import UserService
from src.general.driver.service import DriverService
from src.general.house.service import HouseService
from src.general.order.service import OrderService
from src.general.auth.service.auth import AuthService


from src.helper.error.schema import ErrorSchema
from src.helper.message.schema import MessageSchema
from src.general.order.schema.order_create import OrderCreateSchema
from src.general.order.schema.order_detail import OrderDetailSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

order_router = APIRouter(prefix="/order")

@order_router.post(
    "/create/",
    tags=[SWAGGER_GROUPS["order"]],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema
        },
        400: {
            "model": ErrorSchema
        },
        401: {
            "model": ErrorSchema
        },
        403: {
            "model": ErrorSchema
        },
        404: {
            "model": ErrorSchema
        },
        500: {
            "model": ErrorSchema
        },
    }
)
async def create_order(order_create_sch: OrderCreateSchema,
                       access_token: str = Depends(oauth2_scheme),
                       db: Session = Depends(get_db),
                       auth_service: AuthService = Depends(AuthService),
                       order_service: OrderService = Depends(OrderService),
                       user_service: UserService = Depends(UserService),
                       driver_service: DriverService = Depends(DriverService),
                       house_service: HouseService = Depends(HouseService)
                       ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Create order) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)
        user = await user_service.get_user_by_id(db, token_data["sub"])

        if not user:
            logger.warning(f"(Create order) User not found with ID {token_data['sub']}")
            raise HTTPException(status_code=404, detail="User not found")

        drivers = await driver_service.get_drivers_by_class(db, order_create_sch.driver_class)

        if not drivers:
            raise HTTPException(status_code=404, detail="No drivers available for the selected class")

        driver = random.choice(drivers)

        house_from_id = await house_service.get_house_id(
            db,
            order_create_sch.house_from_street,
            order_create_sch.house_from_building,
            order_create_sch.house_from_number
        )

        house_to_id = await house_service.get_house_id(
            db,
            order_create_sch.house_to_street,
            order_create_sch.house_to_building,
            order_create_sch.house_to_number
        )

        if not house_from_id or not house_to_id:
            raise HTTPException(status_code=400, detail="Invalid departure or arrival location")

        order = await order_service.create_order(
            db=db,
            user_id=user.id,
            driver_id=driver.id,
            order_create_sch=order_create_sch,
            house_from_id=house_from_id,
            house_to_id=house_to_id,
            car=driver.car
        )

        logger.info(f"(Create order) Order successfully created {order.id}")
        return MessageSchema(messageDigest=str(order.id),
                             description="Order successfully created"
                             )
    except jwt.PyJWTError as e:
        logger.warning(f"(Create order) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Create order) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@order_router.get(
    "/{order_id}/",
    tags=[SWAGGER_GROUPS["order"]],
    response_model=OrderDetailSchema,
    responses={
        200: {
            "model": OrderDetailSchema
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
async def get_order_by_id(order_id: int,
                          db: Session = Depends(get_db),
                          access_token: str = Depends(oauth2_scheme),
                          auth_service: AuthService = Depends(AuthService),
                          order_service: OrderService = Depends(OrderService)
                          ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get order find by id) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        order = await order_service.get_order_by_id(db, order_id)

        if not order:
            logger.warning(f"(Get order find by id) order not found: {order.id}")
            raise HTTPException(status_code=404, detail="House not found")

        logger.info(f"(Get order find by id) order successful found: {order.id}")

        return OrderDetailSchema(
            id = order.id,
            user_id = order.user_id,
            driver_id = order.driver_id,
            driver_class = order.driver_class,
            car = order.car,
            house_from_id = order.house_from_id,
            house_from_street = order.house_from_street,
            house_from_building = order.house_from_building,
            house_from_number = order.house_from_number,
            house_to_id = order.house_to_id,
            house_to_street = order.house_to_street,
            house_to_building = order.house_to_building,
            house_to_number = order.house_to_number,
            order_time = order.order_date
        )
    except jwt.PyJWTError as e:
        logger.warning(f"(Get order find by id) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get order find by id) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@order_router.get(
    "/",
    tags=[SWAGGER_GROUPS["order"]],
    response_model=list[OrderDetailSchema],
    responses={
        200: {
            "model": list[OrderDetailSchema]
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
async def get_orders(db: Session = Depends(get_db),
                     access_token: str = Depends(oauth2_scheme),
                     auth_service: AuthService = Depends(AuthService),
                     order_service: OrderService = Depends(OrderService)
                     ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get orders) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        orders = await order_service.get_orders(db)

        logger.info(f"(Get orders) Successful get orders")

        orders_schema = []

        for order in orders:
            orders_schema.append(
                OrderDetailSchema(
                    id=order.id,
                    user_id=order.user_id,
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
        logger.warning(f"(Get orders) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get orders) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")