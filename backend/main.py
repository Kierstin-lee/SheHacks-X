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
 
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from models import ClothingItem, OutfitRequest, OutfitResponse
from outfit_selector import generate_outfit
from storage import get_closet, add_item
from ai_interface import analyze_clothing_image, generate_reasoning, suggest_accessories, suggest_makeup
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
# uploads a photo of a clothing item
@app.post("/clothing/upload", response_model=ClothingItem)
async def upload_clothing(image: UploadFile = File(...)):
    
    image_bytes = await image.read()

    # AI vision analysis(system 1) "What clothing item is this?"
    ai_tags = analyze_clothing_image(image_bytes)

    # Normalize AI output - converts AI guesses into controlled categories
    clean_item = normalized_item(ai_tags)

    # Store item
    stored_item = add_item(clean_item)

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
    reasoning = generate_reasoning (outfit, request.temperature, request.occasion.value, request.preferences)

    return OutfitResponse(
        outfit=outfit,
        reasoning=reasoning,
        makeup=makeup,
        accessories=accessories
    )
