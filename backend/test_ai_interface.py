from ai_interface import analyze_clothing_image, explain_outfit

# Use a publicly accessible image URL
image_url = "https://shop.nirvana.com/products/in-utero-graphic-tee?srsltid=AfmBOopSuothw_KBDDA5l9yFDnYCCnzMLkDtYFDUNWazO7g0IflbAful"

# 1️⃣ Test AI image analysis
tags = analyze_clothing_image(image_url)
print("AI tags:", tags)

# 2️⃣ Test reasoning
temperature = 10
occasion = "casual"
preferences = ["comfortable", "neutral"]
print(explain_outfit({}, temperature, occasion, preferences))