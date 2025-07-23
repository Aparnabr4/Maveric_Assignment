from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from src.schemas import ItemCreate, ItemResponse
from src.database import get_db
from src import models
from typing import List
from src.utils.rate_limiter import limiter


router = APIRouter(tags=['items'], prefix="/items")

# Create item
@router.post('/create', status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_item(request: Request, req: ItemCreate, db: Session = Depends(get_db)):
    new_item = models.Items(item_name=req.item_name, item_description=req.item_description, item_price=req.item_price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# Fetch item by ID
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ItemResponse)
@limiter.limit("5/minute")
def fetch_item_by_id(request: Request, id: int,  db: Session = Depends(get_db)):
    item = db.query(models.Items).filter(models.Items.item_id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Fetch all items
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ItemResponse])
@limiter.limit("5/minute")
def fetch_all_items(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Items).all()

# Update item by ID
@router.put('/{id}', status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def update_item(request: Request, id: int, req: ItemCreate, db: Session = Depends(get_db)):
    item = db.query(models.Items).filter(models.Items.item_id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.item_name = req.item_name
    item.item_description = req.item_description
    item.item_price = req.item_price

    db.commit()
    db.refresh(item)
    return item

# Delete item by ID
@router.delete('/{id}', status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def delete_item(request: Request, id: int, db: Session = Depends(get_db)):
    item = db.query(models.Items).filter(models.Items.item_id == id).first()
    if not item:
        raise HTTPException(status_code=204, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"detail": f"Item with id {id} was deleted successfully"}