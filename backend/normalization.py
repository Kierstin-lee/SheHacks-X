# normalization.py - Cleans up the AI output

from models import ClothingItem, ClothingType, Season, Occasion

def normalize_item(ai_tags: dict) -> ClothingItem:
    """
    Converts AI tags into a fully typed ClothingItem object.
    Fallbacks applied if AI returns unexpected values.
    """
    from uuid import uuid4

    type_map = {"top": "top", "bottom": "bottom", "shoes": "shoes", "outerwear": "outerwear"}
    season_map = {"winter":"winter", "spring":"spring", "summer":"summer", "fall":"fall"}
    occasion_map = {"casual":"casual", "formal":"formal", "business":"business",
                    "athletic":"athletic", "party":"party"}

    clothing_type = type_map.get(ai_tags.get("type", "").lower(), "top")
    seasons = [season_map.get(s.lower(), "summer") for s in ai_tags.get("season", ["summer"])]
    occasions = [occasion_map.get(o.lower(), "casual") for o in ai_tags.get("occasion", ["casual"])]
    color = ai_tags.get("color", "neutral")

    return ClothingItem(
        id=str(uuid4()),
        type=clothing_type,
        color=color,
        season=seasons,
        occasion=occasions
    )