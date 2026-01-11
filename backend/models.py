#models.py - Base models for the "backbone" of the app

from pydantic import BaseModel # library to allow FastAPI to validate and serialize data automatically
from typing import List, Optional

# Represents a single piece of clothing in the closet
class ClothingItem(BaseModel):
    id: str
    image_url: str
    type: str #top, bottom, shoes, outerwear, accessory
    color: str
    season: List[str] #winter, fall, spring, summer
    occasion: List[str] #casual, formal, party, work, athletic, others?

# What the user sends to the backend when they want an outfit
class OutfitRequest(BaseModel):
    temperature: int
    occasion: str
    preferences: List[str] #comfortable, modest, neutral/bright colours, others?

# What the backend sends back the frontend after generating an outfit
class OutfitResponse(BaseModel):
    outfit: dict #keys: top, bottom, shoes, outerwear?(temp dependent)
    accessories: List[ClothingItem]
    makeup: str
    reasoning: str 
