# storage.py - Temporary in-memory closet

from models import ClothingItem
from typing import List

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