# storage.py - Temporary in-memory closet blah

from models import ClothingItem
from typing import List
from fastapi import HTTPException

# In-memory closet
CLOSET: List[ClothingItem] = []

def add_item(item: ClothingItem) -> ClothingItem:
    """
    Adds a clothing item to the in-memory closet.
    """
    CLOSET.append(item)
    return item

def get_closet() -> List[ClothingItem]:
    """
    Returns all items currently in the closet.
    """
    return CLOSET

def update_item(item_id: str, updated_fields: dict):
    """
    Updates an existing ClothingItem in the CLOSET.
    """
    for i, item in enumerate(CLOSET):
        if item.id == item_id:
            for key, value in updated_fields.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            CLOSET[i] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")