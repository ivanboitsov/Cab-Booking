import logging
import jwt

from sqlalchemy.orm import Session
from src.db.database import get_db

from src.config import oauth2_scheme, SWAGGER_GROUPS
from fastapi import APIRouter, Depends, HTTPException

from src.auth.service.auth import AuthService
from src.driver.enum.DriverClassEnum import DriverClassEnum
from src.driver.service import DriverService
from src.driver.schema.driver import DriverSchema
from src.driver.schema.driver_create import DriverCreateSchema

from src.error.schema import ErrorSchema
from src.message.schema import MessageSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

driver_router = APIRouter(prefix="/driver")

@driver_router.post(
    "/",
    tags=[SWAGGER_GROUPS["driver"]],
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
async def create_driver(driver_sch: DriverCreateSchema,
                        db: Session = Depends(get_db),
                        access_token: str = Depends(oauth2_scheme),
                        auth_service: AuthService = Depends(AuthService),
                        driver_service: DriverService = Depends(DriverService)
                        ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get drivers) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        driver = await driver_service.create_driver(db, driver_sch.name, driver_sch.tel, driver_sch.car, driver_sch.driver_class)

        logger.info(f"(Create driver) Driver successful created {driver.id}")
        return MessageSchema(messageDigest=str(driver.id),
                             description="Driver create successfully"
                             )
    except jwt.PyJWTError as e:
        logger.warning(f"(Get driver find by id) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except ValueError as validation_error:
        logger.warning(f"(Create driver) Validation error: {validation_error}")
        raise HTTPException(status_code=400, detail=str(validation_error))
    except Exception as e:
        logger.error(f"(Create driver) Error {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@driver_router.get(
    "/{driver_id}",
    tags=[SWAGGER_GROUPS["driver"]],
    response_model=DriverSchema,
    responses={
        200: {
            "model": DriverSchema
        },
        401: {
            "model": ErrorSchema
        },
        403:{
            "model": ErrorSchema
        },
        404: {
            "model": ErrorSchema
        },
        500:{
            "model": ErrorSchema
        }
    }
)
async def get_driver_by_id(driver_id: int,
                          db: Session = Depends(get_db),
                          access_token: str = Depends(oauth2_scheme),
                          auth_service: AuthService = Depends(AuthService),
                          driver_service: DriverService = Depends(DriverService)
                          ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get driver find by id) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        driver = await driver_service.get_driver_by_id(db, driver_id)

        if not driver:
            logger.warning(f"(Get driver find by id) driver not found: {driver.id}")
            raise HTTPException(status_code=404, detail="driver not found")

        logger.info(f"(Get driver find by id) driver successful found: {driver.id}")

        return DriverSchema(
            id = driver.id,
            name = driver.name,
            tel = driver.tel,
            car = driver.car,
            driver_class = driver.driver_class
        )
    except jwt.PyJWTError as e:
        logger.warning(f"(Get driver find by id) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get driver find by id) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@driver_router.get(
    "/",
    tags=[SWAGGER_GROUPS["driver"]],
    response_model=list[DriverSchema],
    responses={
        200: {
            "model": list[DriverSchema]
        },
        401: {
            "model": ErrorSchema
        },
        403:{
            "model": ErrorSchema
        },
        404: {
            "model": ErrorSchema
        },
        500:{
            "model": ErrorSchema
        }
    }
)
async def get_drivers(db: Session = Depends(get_db),
                      access_token: str = Depends(oauth2_scheme),
                      auth_service: AuthService = Depends(AuthService),
                      driver_service: DriverService = Depends(DriverService)
                      ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get drivers) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        drivers = await driver_service.get_drivers(db)

        logger.info(f"(Get drivers) Successful get drivers")

        drivers_schema = []

        for driver in drivers:
            drivers_schema.append(
                DriverSchema(
                    id=driver.id,
                    name=driver.name,
                    tel=driver.tel,
                    car=driver.car,
                    driver_class=driver.driver_class
                )
            )

        return drivers_schema
    except jwt.PyJWTError as e:
        logger.warning(f"(Get drivers) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get drivers) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@driver_router.get(
    "/class/{driver_class}",
    tags=[SWAGGER_GROUPS["driver"]],
    response_model=list[DriverSchema],
    responses={
        200: {
            "model": list[DriverSchema]
        },
        401: {
            "model": ErrorSchema
        },
        403: {
            "model": ErrorSchema
        },
        500: {
            "model": ErrorSchema
        }
    }
)
async def get_drivers_by_class(driver_class: DriverClassEnum,
                               db: Session = Depends(get_db),
                               access_token: str = Depends(oauth2_scheme),
                               auth_service: AuthService = Depends(AuthService),
                               driver_service: DriverService = Depends(DriverService)
                               ):
    try:

        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get drivers by class) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        drivers_by_class = await driver_service.get_drivers_by_class(db, driver_class)

        logger.info(f"(Get drivers by class) Successful get drivers by class {driver_class}")

        drivers_by_class_schema = []

        for driver in drivers_by_class:
            drivers_by_class_schema.append(
                DriverSchema(
                    id=driver.id,
                    name=driver.name,
                    tel=driver.tel,
                    car=driver.car,
                    driver_class=driver.driver_class
                )
            )

        return drivers_by_class_schema
    except Exception as e:
        logger.error(f"(Get drivers by class) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@driver_router.get(
    "/car/{car}",
    tags=[SWAGGER_GROUPS["driver"]],
    response_model=list[DriverSchema],
    responses={
        200: {
            "model": list[DriverSchema]
        },
        401: {
            "model": ErrorSchema
        },
        403: {
            "model": ErrorSchema
        },
        500: {
            "model": ErrorSchema
        }
    }
)
async def get_drivers_by_class(car: str,
                               db: Session = Depends(get_db),
                               access_token: str = Depends(oauth2_scheme),
                               auth_service: AuthService = Depends(AuthService),
                               driver_service: DriverService = Depends(DriverService)
                               ):
    try:

        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get drivers by car) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        drivers_by_car = await driver_service.get_drivers_by_car(db, car)

        logger.info(f"(Get drivers by car) Successful get drivers which user the {car}")

        drivers_by_car_schema = []

        for driver in drivers_by_car:
            drivers_by_car_schema.append(
                DriverSchema(
                    id=driver.id,
                    name=driver.name,
                    tel=driver.tel,
                    car=driver.car,
                    driver_class=driver.driver_class
                )
            )

        return drivers_by_car_schema
    except Exception as e:
        logger.error(f"(Get drivers by car) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")