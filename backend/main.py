# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ClothingItem, OutfitRequest, OutfitResponse

# Temp title
app = FastAPI(title="My Wardrobe App")

# 1. CORS, so frontend can talk to backend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 2. Sample closet, for testing
sample_closet = [
    ClothingItem(id="1", image_url="top1.png", type="top", color="white", season="summer", occasion=["casual"]),
    ClothingItem(id="2", image_url="bottom1.png", type="bottom", color="blue", season="summer", occasion=["casual", "work"]),
    ClothingItem(id="3", image_url="shoes1.png", type="shoes", color="white", season="summer", occasion=["casual", "athletic"]),
    ClothingItem(id="4", image_url="outerwear1.png", type="outerwear", color="brown", season="winter", occasion=["casual", "work"]),
]

# 3. Root endpoint (existing)
@app.get("/")
def root():
    return {"status": "backend running"}

# 4. Outfit generator endpoint
@app.post("/outfits/generate", response_model=OutfitResponse)
def generate_outfit(request: OutfitRequest):
    # For now: return a fixed outfit
    outfit = {
        "top": sample_closet[0],
        "bottom": sample_closet[1],
        "shoes": sample_closet[2],
        "outerwear": None
    }
    accessories = [sample_closet[3]]

    return OutfitResponse(
        outfit=outfit,
        accessories=accessories,
        makeup="natural makeup",
        reasoning=f"This outfit balances comfort and style for {request.temperature}°C and a {request.occasion} occasion."
    )
