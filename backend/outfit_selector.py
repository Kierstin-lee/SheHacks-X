# outfit_selector.py = This is a Mock up that (as of now) does not use AI decision making

from typing import List
from models import ClothingItem, OutfitRequest, OutfitResponse

# Sample closet
CLOSET: List[ClothingItem] = [
    ClothingItem(id="1", image_url="top1.png", type="top", color="white", season="summer", occasion=["casual"]),
    ClothingItem(id="2", image_url="bottom1.png", type="bottom", color="blue", season="summer", occasion=["casual", "work"]),
    ClothingItem(id="3", image_url="shoes1.png", type="shoes", color="white", season="summer", occasion=["casual", "athletic"]),
    ClothingItem(id="4", image_url="outerwear1.png", type="outerwear", color="brown", season="winter", occasion=["casual", "work"]),
]

def select_Outfit(request: OutfitRequest) -> OutfitResponse:
    # Simple rule-based selection
    outfit_items = {}
    accessories = []

    # Filter by occasion
    candidates = [item for item in CLOSET if request.occasion in item.occasion]

    # Select top
    tops = [item for item in candidates if item.type == "top"]
    outfit_items["top"] = tops[0] if tops else None

    # Select bottom
    bottoms = [item for item in candidates if item.type == "bottom"]
    outfit_items["bottom"] = bottoms[0] if bottoms else None

    # Select shoes
    shoes = [item for item in candidates if item.type == "shoes"]
    outfit_items["shoes"] = shoes[0] if bottoms else None

    # Select outerwear (if cold)
    if request.temperature <= 0:
        outerwear = [item for item in candidates if item.type == "outerwear"]
        outfit_items["outerwear"] = outerwear[0] if outerwear else None

    # Select accessory (might have to change this)
    accessories = [item for item in candidates if item.type == "accessories"][:2]

    # Mock reasoning
    reason = "This outfit balances style and comfort based on temperature and occasion"

    return OutfitResponse(
        outfit=outfit_items,
        accessories=accessories,
        makeup="natural makeup",
        reasoning=reason
    )