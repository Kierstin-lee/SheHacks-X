# outfit_selector.py - Rules + scoring + variation

from typing import List, Optional, Dict
from models import ClothingItem, OutfitRequest, Outfit

import random

# Sample closet (for testing purposes)
CLOSET: List[ClothingItem] = [
    ClothingItem(id="1", image_url="top1.png", type="top", color="white", season="summer", occasion=["casual"]),
    ClothingItem(id="2", image_url="bottom1.png", type="bottom", color="blue", season="summer", occasion=["casual", "work"]),
    ClothingItem(id="3", image_url="shoes1.png", type="shoes", color="white", season="summer", occasion=["casual", "athletic"]),
    ClothingItem(id="4", image_url="outerwear1.png", type="outerwear", color="brown", season="winter", occasion=["casual", "work"]),
]

# Weather/temperature converter
def get_weather_category(temp: int) -> str:
    if temp <= 0:
        return "cold"
    elif temp <= 15:
        return "mild"
    else:
        return "hot"
    
# Score items
def score_items(items: List[ClothingItem], occasion: str, preferences: List[str]) -> List[Dict]:
    scored = []
    for item in items:
        score = 0
        # Match occasion
        if occasion in item.occasion:
            score += 2

        # Simple preference scoring (comfortable favors sneakers/sweats)
        if "comfortable" in preferences and item.type in ["top", "bottom", "shoes"]:
            score += 1

        # Match season
        if season in item.season:
            score += 3     

        scored.append({"item": item, "score": score, "season": season})

    # Sort descending
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

# Pick top candidates wtih randomness
def choose_top(scored_list: List[Dict]) -> Optional[ClothingItem]:
    if not scored_list:
        return None
    top_candidates = scored_list[:3]  
    return random.choice(top_candidates)["item"]

# Determine if outerwear should be included or not
def select_outerwear(items: List[ClothingItem], weather:str) -> Optional[ClothingItem]:
    outerwear_items = [i for i in items if i.type == "outerwear"]
    if not outerwear_items:
        return None
    if weather == "cold":
        return outerwear_items[0]  # must include
    elif weather == "mild":
        return random.choice([outerwear_items[0], None])  # optional
    else:
        return None  # hot → no outerwear

# Main outfit selection function
def generatwe_outfits(request: OutfitRequest) -> Dict[str, Optional[ClothingItem]]:
    weather = get_weather_category(request.temperature)

    # Filter closet by occasion and exclude_item_ids
    candidates = [i for i in CLOSET if request.occasion.value in i.occasion and i.id not in request.exclude_item_ids]

    # Separate by type
    tops = [i for i in candidates if i.type == "top"]
    bottoms = [i for i in candidates if i.type == "bottom"]
    shoes = [i for i in candidates if i.type == "shoes"]

    outfit = {
        "top": choose_top(score_items(tops, request.occasion.value, request.preferences)),
        "bottom": choose_top(score_items(bottoms, request.occasion.value, request.preferences)),
        "shoes": choose_top(score_items(shoes, request.occasion.value, request.preferences)),
        "outerwear": select_outerwear(candidates, weather)
    }

    return outfit