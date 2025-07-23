from  src.database import Base
from sqlalchemy import Column, Integer, String

class Items(Base):
    __tablename__ = "Items"

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    item_description = Column(String, nullable=False)
    item_price = Column(Integer, nullable=False)