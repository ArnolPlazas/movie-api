from config.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    last_name = Column(String)
    country = Column(String)
    email = Column(String)