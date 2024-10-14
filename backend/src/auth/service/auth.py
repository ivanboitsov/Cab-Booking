import logging
import jwt

from datetime import datetime, timedelta

from debugpy.adapter.sessions import Session
from passlib.context import CryptContext

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET_KEY
from src.auth.models import CRL

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.TOKEN_LIFETIME = int(ACCESS_TOKEN_EXPIRE_MINUTES)
        self.SECRET_KEY = str(JWT_SECRET_KEY)
        self.ALGORITHM = str(ALGORITHM)

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verify_hashed_password(plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)

    async def create_access_token(self, data: dict) -> str:
        try:
            to_encode = data.copy()
            expire_delta = timedelta(minutes=self.TOKEN_LIFETIME)
            expire = datetime.now() + expire_delta
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

            self.logger.info(f"(Create access token) Successful created access token with payload: {data}")

            return encoded_jwt
        except Exception as e:
            self.logger.error(f"(Create access token) Error creating access token: {e}")
            raise

    async def get_data_from_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            self.logger.info(f"(Get data from token) Successful get data: {payload}")
            return payload
        except jwt.PyJWTError as e:
            self.logger.warning(f"(Get data from token) Bad auth token: {token}")
            raise
        except Exception as e:
            self.logger.error(f"(Get data from token) Error auth token: {e}")
            raise

    async def revoke_access_token(self, db: Session, token: str) -> None:
        try:
            crl_entry = CRL(token=token)
            db.add(crl_entry)
            db.commit()
            self.logger.info(f"(Revoke access token) Token revoked: {token}")
        except Exception as e:
            self.logger.error(f"(Revoke access token) Error token revoked: {e}")

    async def check_revoked(self, db: Session, token: str) -> bool:
        try:
            if db.query(CRL).filter(CRL.token == token).first():
                self.logger.warning(f"(Check revoked access token) Token revoked: {token}")
                return True
            else:
                self.logger.warning(f"(Check revoked access token) Token not revoked: {token}")
                return False
        except Exception as e:
            self.logger.error(f"(Check revoked access token) Error revoking token: {e}")