# models.py - Base models for the "backbone" of the app (Pydantic schemas)
# the rule book blah

from pydantic import BaseModel # library to allow FastAPI to validate and serialize data automatically
from typing import List, Optional, Dict
from enum import Enum

# Enums = Prevents AI weirdness and typos
class ClothingType(str, Enum):
    top = "top"
    bottom = "bottom"
    shoes = "shoes"
    outerwear = "outerwear"

class Season(str, Enum):
    winter = "winter"
    spring = "spring"
    summer = "summer"
    fall = "fall"

class Occasion(str, Enum):
    casual = "casual"
    formal = "formal"
    business = "business"
    athletic = "athletic"
    party = "party"          

# Represents a single piece of clothing in the closet
class ClothingItem(BaseModel):
    id: str
    image_url: Optional[str] = None

    type: ClothingType
    subtype: Optional[str] = None
    color: str

    season: List[Season]
    occasion: List[Occasion]

    confidence: Optional[float] = None

class Outfit(BaseModel):
    top: Optional[ClothingItem] = None
    bottom: Optional[ClothingItem] = None
    shoes: Optional[ClothingItem] = None
    outerwear: Optional[ClothingItem] = None    

# What the user sends to the backend when they want an outfit
class OutfitRequest(BaseModel):
    temperature: int
    occasion: Occasion
    preferences: List[str] #comfortable, modest, neutral/bright colours, others?
    exclude_item_ids: Optional[List[str]] = []

# What the backend sends back the the frontend after generating an outfit
class OutfitResponse(BaseModel):
    outfit: Dict[str, Optional[ClothingItem]] #keys: top, bottom, shoes, outerwear?(temp dependent)
    accessories: List[str]
    makeup: str
    reasoning: str 