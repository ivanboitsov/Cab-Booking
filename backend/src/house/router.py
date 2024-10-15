import logging
import jwt

from sqlalchemy.orm import Session
from src.db.database import get_db

from src.config import oauth2_scheme, SWAGGER_GROUPS
from fastapi import APIRouter, Depends, HTTPException

from src.house.service import HouseService
from src.auth.service.auth import AuthService
from src.house.schema.house import HouseSchema

from src.error.schema import ErrorSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

house_router = APIRouter(prefix="/house")

@house_router.get(
    "/{house_id}",
    tags=[SWAGGER_GROUPS["house"]],
    response_model=HouseSchema,
    responses={
        200: {
            "model": HouseSchema
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
async def get_house_by_id(house_id: int,
                          db: Session = Depends(get_db),
                          access_token: str = Depends(oauth2_scheme),
                          auth_service: AuthService = Depends(AuthService),
                          house_service: HouseService = Depends(HouseService)
                          ):
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get house find by id) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        house = await house_service.get_house_by_id(db, house_id)

        if not house:
            logger.warning(f"(Get house find by id) House not found: {house.id}")
            raise HTTPException(status_code=404, detail="House not found")

        logger.info(f"(Get house find by id) House successful found: {house.id}")

        return HouseSchema(
            id = house.id,
            street = house.street,
            building = house.building,
            number = house.number
        )
    except jwt.PyJWTError as e:
        logger.warning(f"(Get house find by id) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get house find by id) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@house_router.get(
    "/",
    tags=[SWAGGER_GROUPS["house"]],
    response_model=list[HouseSchema],
    responses={
        200: {
            "model": list[HouseSchema]
        },
        401: {
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
async def get_houses(access_token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db),
                     auth_service: AuthService = Depends(AuthService),
                     house_service: HouseService = Depends(HouseService)
                     ):
    try:

        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get houses) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        houses = await house_service.get_houses(db)

        logger.info(f"(Get houses) Successful get houses")

        houses_schema = []

        for house in houses:
            houses_schema.append(
                HouseSchema(
                    id = house.id,
                    street = house.street,
                    building = house.building,
                    number = house.number
                )
            )

        return houses_schema
    except jwt.PyJWTError as e:
        logger.warning(f"(Get houses) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get houses) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")