# routes/item_routes.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from models.item_model import Item as ItemModel
from database import get_db
from controllers.item_controller import (
    create_item_service,
    get_item_service,
    update_item_service,
    delete_item_service,
)

router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(ItemCreate):
    id: int

@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item."""
    db_item = create_item_service(db=db, item_data=item.dict())
    return db_item

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieve a single item by ID."""
    item = get_item_service(db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    """Update an item by ID."""
    updated_item = update_item_service(db=db, item_id=item_id, item_data=item.dict())
    return updated_item

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item by ID."""
    delete_item_service(db=db, item_id=item_id)
    return {"message": "Item deleted successfully"}
