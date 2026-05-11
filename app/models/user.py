from app.database import Base
from sqlalchemy import Column, String, Integer



class User(Base):
    __tablename__ = 'users'


    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
