import logging
from typing import Optional, List

from sqlalchemy.orm import Session

from src.general.order.models import Order
from src.general.order.schema.order_create import OrderCreateSchema


class OrderService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def create_order(self,
                           user_id,
                           driver_id,
                           order_create_sch: OrderCreateSchema,
                           house_from_id,
                           house_to_id,
                           car,
                           db: Session):
        try:
            new_order = Order(
                user_id = user_id,
                driver_id = driver_id,
                house_from_id = house_from_id,
                house_from_street = order_create_sch.house_from_street,
                house_from_building=order_create_sch.house_from_building,
                house_from_number=order_create_sch.house_from_number,
                house_to_id=house_to_id,
                house_to_street = order_create_sch.house_to_street,
                house_to_building=order_create_sch.house_to_building,
                house_to_number=order_create_sch.house_to_number,
                driver_class = order_create_sch.driver_class,
                car = car
            )

            db.add(new_order)
            db.commit()
            db.refresh(new_order)

            self.logger.info(f"(Create order) Success: {new_order}")
            return new_order

        except Exception as e:
            db.rollback()
            self.logger.error(f"(Create order) Error {e}")

    async def get_order_by_id(self, db:Session, order_id: int) -> Optional[Order]:
        try:
            order = db.query(Order).filter(Order.id == order_id).first()

            if order:
                self.logger.info(f"(Get order by ID) Found order with ID {order_id}")
            else:
                self.logger.info(f"(Get order by ID) No house order with ID {order_id}")

            return order
        except Exception as e:
            self.logger.error(f"(Get order by ID) Error: {e}")
            raise

    async def get_user_orders(self, db: Session, user_id: int) -> List[Order]:
        try:
            orders = db.query(Order).filter(Order.user_id == user_id).all()
            self.logger.info(f"(Get user orders) Retrieved user {len(orders)} orders")

            return orders
        except Exception as e:
            self.logger.error(f"(Get user orders) Error: {e}")
            raise

    async def get_driver_orders(self, db: Session, driver_id: int) -> List[Order]:
        try:
            orders = db.query(Order).filter(Order.driver_id == driver_id).all()
            self.logger.info(f"(Get driver orders) Retrieved driver {len(orders)} orders")

            return orders
        except Exception as e:
            self.logger.error(f"(Get driver orders) Error: {e}")
            raise

    async def get_orders(self, db: Session) -> List[Order]:
        try:
            orders = db.query(Order).all()
            self.logger.info(f"(Get orders) Retrieved {len(orders)} orders")

            return orders
        except Exception as e:
            self.logger.error(f"(Get orders) Error: {e}")
            raise