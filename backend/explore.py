import requests
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

explore_bp = Blueprint("explore", __name__)

# API keys and URLs
PERENUAL_API_KEY = os.getenv("PERENUAL_API_KEY")
PLANT_ID_API_KEY = os.getenv("PLANT_ID_API_KEY")
PERENUAL_BASE_URL = "https://perenual.com/api/v2/species-list"
PLANT_ID_SEARCH_URL = "https://plant.id/api/v3/kb/plants/name_search"
PLANT_ID_DETAILS_URL = "https://plant.id/api/v3/kb/plants"

@explore_bp.route("/recommendations", methods=["GET"])
def get_recommendations():
    # Get user input (e.g., from query parameters)
    hardiness_zone = request.args.get("hardiness", type=int)
    sunlight = request.args.get("sunlight", type=str)

    if not hardiness_zone or not sunlight:
        return jsonify({"error": "Hardiness zone and sunlight are required"}), 400

    # Step 1: Fetch plants from Perenual API
    perenual_plants = fetch_perenual_plants(hardiness_zone, sunlight)
    if not perenual_plants:
        return jsonify({"error": "Failed to fetch plants from Perenual API"}), 500

    # Step 2: Fetch plant details from Plant.id API
    recommended_plants = []
    for plant in perenual_plants:
        plant_id = plant["id"]
        scientific_name = plant["scientific_name"][0]  # Take the first scientific name

        # Fetch access token from Plant.id
        access_token = fetch_plant_id_access_token(scientific_name)
        if not access_token:
            continue  # Skip if no access token found

        # Fetch plant details from Plant.id
        plant_details = fetch_plant_id_details(access_token)
        if not plant_details:
            continue  # Skip if no details found

        # Fetch additional details from Perenual
        perenual_details = fetch_perenual_plant_details(plant_id)
        if not perenual_details:
            continue  # Skip if no details found

        # Combine data
        recommended_plants.append({

            "common_name": perenual_details.get("common_name", ""),
            "scientific_name": scientific_name,
            "picture": plant_details.get("image", ""),
            
            
            "best_soil_type": plant_details.get("best_soil_type", ""),
            "best_watering": plant_details.get("best_watering", ""),
            "watering": perenual_details.get("watering", "")
        })

    return jsonify({"recommended_plants": recommended_plants})

def fetch_perenual_plants(hardiness_zone, sunlight):
    """Fetch plants from Perenual API based on hardiness zone and sunlight."""
    plants = []
    page = 1
    max_plants = 150

    while len(plants) < max_plants:
        params = {
            "key": PERENUAL_API_KEY,
            "hardiness": hardiness_zone,
            "sunlight": sunlight,
            "page": page
        }
        response = requests.get(PERENUAL_BASE_URL, params=params)
        if response.status_code != 200:
            break

        data = response.json()
        for plant in data.get("data", []):
            if plant["id"] > 3000:
                continue  # Skip plants with ID > 3000
            if "'" in plant["scientific_name"][0]:
                continue  # Skip plants with specific names (e.g., 'Kasagi Yama')
            plants.append(plant)

        if data.get("last_page", 0) <= page:
            break  # No more pages
        page += 1

    return plants[:max_plants]  # Return up to max_plants

def fetch_plant_id_access_token(scientific_name):
    """Fetch access token from Plant.id API using scientific name."""
    params = {"q": scientific_name}
    headers = {
        "Api-Key": PLANT_ID_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(PLANT_ID_SEARCH_URL, headers=headers, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    if data.get("entities"):
        return data["entities"][0]["access_token"]  # Take the first match
    return None

def fetch_plant_id_details(access_token):
    """Fetch plant details from Plant.id API using access token."""
    url = f"{PLANT_ID_DETAILS_URL}/{access_token}?details=best_soil_type,best_watering,image"
    headers = {
        "Api-Key": PLANT_ID_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    return response.json()

def fetch_perenual_plant_details(plant_id):
    """Fetch additional plant details from Perenual API using plant ID."""
    url = f"https://perenual.com/api/v2/species/details/{plant_id}?key={PERENUAL_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    return response.json()