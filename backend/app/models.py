from sqlalchemy import Column, Integer, String
from .database import Base


class UserCredential(Base):
    __tablename__ = "user_credentials"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    original_password = Column(String)
    result = Column(String)  # cracked / failed / pending
