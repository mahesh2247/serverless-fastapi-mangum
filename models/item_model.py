# models/item_model.py

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from database import Base

# SQLAlchemy Item model
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)

    def to_dict(self):
        """Convert SQLAlchemy Item instance to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }

# Pydantic models for validation and serialization
class ItemBase(BaseModel):
    name: str
    description: str = None
    price: float

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True  # Change this to from_attributes
