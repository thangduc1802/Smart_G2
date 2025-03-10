import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

# ✅ .env laden
load_dotenv()

weather_bp = Blueprint("weather_bp", __name__)

# ✅ OpenWeather API-Key aus .env laden
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@weather_bp.route("/", methods=["GET"])
def get_weather():
    city = request.args.get("city", "Berlin")  # Standard: Berlin
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Wetterdaten nicht verfügbar"}), 500
