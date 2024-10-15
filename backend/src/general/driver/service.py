import logging

from typing import List, Optional

from sqlalchemy.orm import Session
from src.general.driver.models import Driver
from src.general.driver.enum.DriverClassEnum import DriverClassEnum


class DriverService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def get_driver_by_id(self, db: Session, _id: int) -> Optional[Driver]:
        try:
            driver = db.query(Driver).filter(Driver.id == _id).first()

            if driver:
                self.logger.info(f"(Get driver by ID) Found driver with ID {_id}")
            else:
                self.logger.info(f"(Get driver by ID) No driver found with ID {_id}")

            return driver
        except Exception as e:
            self.logger.error(f"(Get driver by ID) Error: {e}")
            raise

    async def get_drivers(self, db: Session) -> List[Driver]:
        try:
            drivers = db.query(Driver).all()
            self.logger.info(f"(Get drivers) Retrieved {len(drivers)} drivers")
            return drivers
        except Exception as e:
            self.logger.error(f"(Get drivers) Error: {e}")
            raise

    async def get_drivers_by_car(self, db: Session, car: str) -> List[Driver]:
        try:
            class_drivers = db.query(Driver).filter(Driver.car == car).all()
            self.logger.info(f"(Get drivers by car) Retrieved {len(class_drivers)} drivers which use car model is {car}")
            return class_drivers
        except Exception as e:
            self.logger.error(f"(Get class by car) Error: {e}")
            raise

    async def get_drivers_by_class(self, db: Session, _class: DriverClassEnum) -> List[Driver]:
        try:
            car_drivers = db.query(Driver).filter(Driver.driver_class == _class).all()
            self.logger.info(f"(Get drivers by class) Retrieved {len(car_drivers)} class {_class} drivers")
            return car_drivers
        except Exception as e:
            self.logger.error(f"(Get drivers by class) Error: {e}")
            raise

    async def create_driver(self, db: Session, name: str, tel: str, car: str, driver_class: DriverClassEnum) -> Driver:
        try:
            driver = Driver(
                name = name,
                tel = tel,
                car = car,
                driver_class = driver_class
            )
            db.add(driver)
            db.commit()
            db.refresh(driver)

            self.logger.info(f"(Creating driver) Success: {driver}")

            return driver
        except Exception as e:
            self.logger.info(f"(Creating driver) Error: {e}")
            raise