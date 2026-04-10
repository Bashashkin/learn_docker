from sqlalchemy import Column, Integer, String
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    status = Column(String)
