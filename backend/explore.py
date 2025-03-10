import requests
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

explore_bp = Blueprint("explore", __name__)

TREFLE_API_KEY = os.getenv("TREFLE_API_KEY")
TREFLE_BASE_URL = "https://trefle.io/api/v1/plants"
PLANT_ID_API_KEY = os.getenv("PLANT_ID_API_KEY")
PLANT_ID_BASE_URL = "https://plant.id/api/v3"
#HArdiness zones
HARDINESS_ZONES = {
    "2": {"min_temp": -45, "max_temp":-40 },
    "3": {"min_temp": -40, "max_temp":-34 },
    "4": {"min_temp": -34, "max_temp":-28 },
    "5": {"min_temp": -28, "max_temp":-23 },
    "6": {"min_temp": -23, "max_temp":-17 },
    "7": {"min_temp": -17, "max_temp":-12 },
    "8": {"min_temp": -12, "max_temp":-6 },
    "9": {"min_temp": -6, "max_temp":-1 },
    "10": {"min_temp": -1, "max_temp":4 },
    "11": {"min_temp": 4, "max_temp":10 },
}


@explore_bp.route("/recommendations", methods=["GET"])  
def get_recommendations():
    #Get user input 
    hardiness_zone = request.args.get("hardiness_zone", type=str)
    light_scale = request.args.get("light_scale", type=int)
    soil_ph = request.args.get("soil_ph", type=float)

    #validate input
    if not hardiness_zone or not light_scale or not soil_ph:
        return jsonify({"error": "Missing required parameters"}), 400

    #check if the server works
    plants = fetch_plants_from_trefle()
    if not plants:
        return jsonify({"error": "Failed to fetch plant data from Trefle"}), 500
    
    #recommend 20 plants
    recommended_plants = []
    for plant in plants:
        min_temp = plant.get("minimum_temparature")
        if not min_temp or not is_in_hardiness_zone(hardiness_zone, min_temp):
            continue

        plant_light = plant.get("light")
        if not plant_light or not is_light_match(light_scale, plant_light):
            continue

        scientific_name = plant.get("scientific_name")
        water_demand = fetch_water_demand_from_plant_id(scientific_name)
        if not water_demand:
            continue  # Skip plants with missing water demand data


        recommended_plants.append({
            "picture": plant.get("image_url"),
            "common_name": plant.get("common_name"),
            "scientific_name": scientific_name,
            "growth_habit": plant.get("growth_habit"),
            "native_to": plant.get("native"),
            "water_demand": water_demand,
            "light_scale": plant_light,
            "temperature_range": {
                "min": plant.get("minimum_temperature"),
                "max": plant.get("maximum_temperature")
            },
            "ph_range": {
                "min": ph_min,
                "max": ph_max
            }
        })

    return jsonify({"recommended_plants": recommended_plants[:20]})

def is_in_hardiness_zone(hardiness_zone, min_temp):
    """Check if the plant's minimum temperature falls within the hardiness zone."""
    zone_data = HARDINESS_ZONE.get(hardniness_zone)
    if not zone_data:
        return False
    return zone_data["min_temp"] <= min_temp <= zone_data["max_temp"]

def is_light_match(user_light, plant_light):
    """Check if the plant's light requirements match the user's input."""
    if user_light <=3:
        return plant_light <=3
    elif 4 <= user_light <= 6:
        return 4 <= plant_light <= 6  
    else:
        return plant_light >= 7  

def is_ph_match(user_ph, ph_min, ph_max):
    """Check if the user's soil pH falls within the plant's acceptable range."""
    return ph_min <= user.ph <= ph_max

def fetch_plants_from_trefle():
    """Fetch plants from Trefle API."""
    try:
        params={
            "token": TREFLE_API_KEY,
            "page_size":100
        }
        response = request.get(TREFLE_BASE_URL, params=params)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching plants from Trefle: {e}")
        return None

def fetch_water_demand_from_plant_id(scientific_name):
    """Fetch water demand from Plant.id API."""
    try:
        headers = {
            "Content-Type": "application/json",
            "Api-Key": PLANT_ID_API_KEY
        }
        data = {
            "details": ["watering"],
            "species": [scientific_name]
        }
        response = requests.post(f"{PLANT_ID_BASE_URL}/species", headers=headers, json=data)
        response.raise_for_status()
        details = response.json().get("plant_details", {})
        watering = details.get("watering")

        if watering:
            min_text = "dry" if watering["min"] == 1 else "medium" if watering["min"] == 2 else "wet"
            max_text = "dry" if watering["max"] == 1 else "medium" if watering["max"] == 2 else "wet"
            return f"{min_text} to {max_text}"

        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching water demand from Plant.id: {e}")
        return None

    

    