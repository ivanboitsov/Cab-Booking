import logging

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.general.auth.router import user_router
from src.general.house.router import house_router
from src.general.driver.router import driver_router
from src.general.order.router import order_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/taksa")

router.include_router(driver_router)
router.include_router(house_router)
router.include_router(user_router)
router.include_router(order_router)

app = FastAPI()

app.include_router(router)

app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)
