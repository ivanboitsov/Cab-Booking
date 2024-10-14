import logging

from typing import List, Optional
from sqlalchemy.orm import Session
from src.house.models import House


class HouseService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def get_house_by_id(self, db: Session, house_id: int) -> Optional[House]:
        try:
            house = db.query(House).filter(House.id == house_id).first()

            if house:
                self.logger.info(f"(Get house by ID) Found house with ID {house_id}")
            else:
                self.logger.info(f"(Get house by ID) No house found with ID {house_id}")

            return house
        except Exception as e:
            self.logger.error(f"(Get house by ID) Error: {e}")
            raise

    async def get_houses(self, db: Session) -> List[House]:
        try:
            houses = db.query(House).all()
            self.logger.info(f"(Get houses) Retrieved {len(houses)} houses")
            return houses
        except Exception as e:
            self.logger.error(f"(Get houses) Error: {e}")
            raise

    async def update_house(self, db: Session, house_id: int, number: str, building: Optional[str], street: str) -> Optional[House]:
        try:
            house = db.query(House).filter(House.id == house_id).first()

            if not house:
                self.logger.info(f"(Update house) No house found with ID {house_id}")
                return None

            if house.number != number or house.building != building or house.street != street:
                house.number = number
                house.building = building
                house.street = street
                db.commit()
                db.refresh(house)
                self.logger.info(f"(Update house) Updated house with ID {house_id}")
            else:
                self.logger.info(f"(Update house) No changes detected for house with ID {house_id}")

            house.number = number
            house.building = building
            house.street = street

            db.commit()
            db.refresh(house)

            self.logger.info(f"(Update house) Updated house with ID {house_id}")

            return house
        except Exception as e:
            self.logger.error(f"(Update house) Error: {e}")
            raise

    async def get_houses_by_street(self, db: Session, street: str) -> List[House]:
        try:
            houses = db.query(House).filter(House.street == street).all()
            self.logger.info(f"(Get houses by street) Retrieved {len(houses)} houses on street {street}")
            return houses
        except Exception as e:
            self.logger.error(f"(Get houses by street) Error: {e}")
            raise