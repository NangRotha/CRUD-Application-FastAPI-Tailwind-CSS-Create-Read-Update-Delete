from sqlalchemy.orm import Session
from typing import List, Optional
from models import Item
from schemas import ItemCreate, ItemUpdate

def get_item(db: Session, item_id: int) -> Optional[Item]:
    """Get a single item by ID"""
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """Get all items with pagination"""
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate) -> Item:
    """Create a new item"""
    db_item = Item(
        title=item.title,
        description=item.description,
        completed=item.completed
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate) -> Optional[Item]:
    """Update an existing item"""
    db_item = get_item(db, item_id)
    if db_item:
        update_data = item.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> bool:
    """Delete an item"""
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False