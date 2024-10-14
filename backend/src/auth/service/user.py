import logging
from typing import List

from git.util import get_user_id
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from src.auth.models import User
from src.auth.service.auth import AuthService

class UserService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def get_user_by_email(self, db: Session, email: str) -> User:
        try:
            user = db.query(User).filter(User.email == email).one_or_none()

            if user:
                self.logger.info(f"(Email user getting) Got user with ID {user.id}")
            else:
                self.logger.info(f"(Email user getting) No same user found: {email}")

            return user
        except Exception as e:
            self.logger.info(f"(Email user getting) Error: {e}")
            raise

    async def get_user_by_id(self, db: Session, _id: int) -> User:
        try:
            user = db.query(User).filter(User.id == _id).first()

            if user:
                self.logger.info(f"(User id getting) Got user with ID {user.id}")
            else:
                self.logger.info(f"(User id getting) No same user found: {_id}")

            return user
        except Exception as e:
            self.logger.info(f"(User id getting) Error: {e}")
            raise

    async def verify_password(self, db: Session, email: str, password: str) -> bool:
        try:
            user = await self.get_user_by_email(db, email)

            if not user:
                self.logger.info(f"(Password verify) No same user found: {email}")
                return False

            if AuthService.verify_hashed_password(password, user.password):
                self.logger.info(f"(Password verify) Success: {email}")
                return True
            else:
                self.logger.info(f"(Password verify) Failure: {email}")
                return False

        except Exception as e:
            self.logger.info(f"(Password verify) Error: {email}")
            raise

    async def create_user(self, db: Session, name: str, tel: str, email: str, password: str) -> User:
        try:
            hashed_password = AuthService.get_hashed_password(password)

            user = User(
                name = name,
                tel = tel,
                email = email,
                password = hashed_password
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            self.logger.info(f"(Creating user) Success: {user}")

            return user
        except Exception as e:
            self.logger.info(f"(Creating user) Error: {e}")
            raise

    async def update_user(self, db: Session, _id: int, name: str, tel: str, email: str) -> User:
        try:
            user = await self.get_user_by_id(db,_id)

            if name:
                user.name = name
            if tel:
                user.tel = tel
            if email:
                user.email = email

            db.commit()
            db.refresh(user)

            self.logger.info(f"(Updating user) Success: {user}")

            return user
        except NoResultFound:
            self.logger.info(f"(Updating user) Error: User with ID {_id} not found")
            raise ValueError(f"User with ID {_id} not found")
        except Exception as e:
            db.rollback()
            self.logger.info(f"(Updating user) Error: {e}")
            raise

    async def get_all_users(self, db: Session) -> List[User]:
        try:
            users = db.query(User).all()
            self.logger.info(f"(Getting all users) Retrieved {len(users)} users")
            return users
        except Exception as e:
            self.logger.info(f"(Getting all users) Error: {e}")
            raise
