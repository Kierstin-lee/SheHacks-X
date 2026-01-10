#ai_interface.py - Vision AI + reasoning text

from dotenv import load_dotenv
import os
import openai
from typing import Dict

# load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Clothing AI: analyze image
# def analyze_clothing_image_bytes(images_bytes: bytes) -> dict:
def analyze_clothing_image(image_url: str) -> Dict:
    prompt = f"""
    Analyze this clothing image: {image_url}

    Return **ONLY** a valid JSON object with these keys:
    {{
        "type": "top/bottom/shoes/outerwear",
        "color": "primary color",
        "season": ["summer","winter","spring","fall"],
        "occasion": ["casual","athletic","formal","work","party"]
    }}

    Do not include any extra text, explanations, or formatting.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a fashion AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        text = response.choices[0].message.content

        # Robust JSON extraction
        import re
        import json
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            ai_tags = json.loads(match.group())
            return normalize_tags(ai_tags)
        else:
            # fallback: try parsing the whole text
            ai_tags = json.loads(text.strip())
            return normalize_tags(ai_tags)

    except Exception as e:
        print("Failed to parse AI JSON:", e)
        print("Raw AI output:", text if 'text' in locals() else "No text returned")
        return None

# Normalize AI output
def normalize_tags(ai_tags):
    """
    Converts raw AI output into standardized, safe values.
    """
    def map_type(t): 
        t = t.lower()
        return t if t in ["top","bottom","shoes","outerwear"] else "top"

    def normalize_color(c):
        if not c:
            return "neutral"
        
        c = c.lower()
        # List of common base colors
        base_colors = ["white","black","blue","red","green","yellow","brown","orange","pink","purple","gray","beige","cream"]

        # Split words and find the first word that matches a base color
        for word in c.split():
            if word in base_colors:
                return word

        # fallback if no match
        return "neutral"

    def normalize_season(seasons):
        valid = ["winter","spring","summer","fall"]
        return [s.lower() for s in seasons if s.lower() in valid] or ["summer"]

    def normalize_occasion(occs):
        valid = ["casual","athletic","formal","work","party"]
        return [o.lower() for o in occs if o.lower() in valid] or ["casual"]

    return {
        "type": map_type(ai_tags.get("type", "top")),
        "color": normalize_color(ai_tags.get("color", "neutral")),
        "season": normalize_season(ai_tags.get("season", ["summer"])),
        "occasion": normalize_occasion(ai_tags.get("occasion", ["casual"]))
    }

# Outfit reasoning generator
def explain_outfit(outfit, temperature, occasion, preferences):
    """
    Generates a human-readable explanation for the selected outfit.
    """
    weather = ""
    if temperature <= 0:
        weather = "cold"
    elif 0 < temperature <= 15:
        weather = "mild"
    else:
        weather = "hot"

    pref_text = ", ".join(preferences) if preferences else "your preferences"

    explanation = (
        f"This outfit was selected based on {occasion} suitability, "
        f"optimized for {weather} weather, "
        f"and aligned with your preferences for {pref_text}."
    )
    return explanation

def suggest_accessories(outfit: dict, occasion: str, preferences: list) -> list:
    return ["necklace", "watch"]

def suggest_makeup(outfit: dict, occasion: str, preferences: list) -> list:
    return ["natural makeup"]