# main.py - *routes and coordinates*, the backend controller for the app balh
# receives requests from the website, sends them to the right AI / logic modules, and returns clean, usable results back to the frontend

from dotenv import load_dotenv
import os
import openai

load_dotenv() # reads the env file

openai.api_key = os.getenv("OPENAI_API_KEY") # Gets the API key

# Tester
if openai.api_key:
    print("OpenAI is successful")
else:
    print("fail")    
 
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4

from models import ClothingItem, OutfitRequest, OutfitResponse
from outfit_selector import generate_outfit
from storage import get_closet, add_item, update_item
from ai_interface import analyze_clothing_image, suggest_accessories, suggest_makeup
from normalization import normalized_item

# App creation, creates the backend server and give the API a name
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

# 2. Root endpoint (existing) - confirms the backend is alive
@app.get("/")
def root():
    return {"status": "backend running"}

# 3. AI System 1 - Image upload & tagging
class ClothingAnalyzeRequest(BaseModel):
    image_url: str

@app.post("/clothing/analyze", response_model=ClothingItem)
def analyze_clothing(req: ClothingAnalyzeRequest):
    """
    Takes an image URL, returns AI predicted tags for review.
    Frontend should display these tags and allow manual override.
    """
    ai_tags = analyze_clothing_image(req.image_url)
    if not ai_tags:
        raise HTTPException(status_code=500, detail="AI analysis failed")
    
    # Normalize tags into ClothingItem object (but do NOT store yet)
    temp_item = ClothingItem(
        id=str(uuid4()),
        image_url=req.image_url,
        type=ai_tags["type"],
        color=ai_tags["color"],
        season=ai_tags["season"],
        occasion=ai_tags["occasion"]
    )
    return temp_item

# NEW Save clothing after manual override
@app.post("/clothing/save", response_model=ClothingItem)
def save_clothing(item: ClothingItem):
    stored_item = add_item(item)
    return stored_item

# 4. AI System 2 - Outfit generator endpoint
@app.post("/outfits/generate", response_model=OutfitResponse)
def generate_outfit(request: OutfitRequest):

    closet = get_closet()
    
    # Generate outfit - filters invalid items(rules), scores items(AI logic), generates one outfit, avoids repeats
    outfit = generate_outfit (
        closet=closet,
        temperature=request.temperature,
        occasion=request.occasion,
        preferences=request.preferences,
        exclude_ids=request.exclude_item_ids
    )

    accessories = suggest_accessories(request.occasion.value)
    makeup = suggest_makeup(request.occasion.value)

    # Uses OpenAI to explain why the outfit was chosen
    reasoning = f"Generated outfit based on {request.occasion.value}, temperature {request.temperature}, preferences {request.preferences}"

    return OutfitResponse (
        outfit=outfit,
        makeup=makeup,
        accessories=accessories,
        reasoning=reasoning
    )

@app.put("/clothing/update/{item_id}", response_model=ClothingItem)
def manual_override(item_id: str, updated_fields: dict = Body(...)):
    """
    Allows the user to manually correct AI tags for a clothing item
    """
    return update_item(item_id, updated_fields)