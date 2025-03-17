import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv  # ✅ Neu: Dotenv importieren
from config import Config
from extensions import db
from auth import auth_bp
from routes.weather import weather_bp
from explore import explore_bp

# ✅ Lade .env-Datei
load_dotenv()

app = Flask(__name__, static_url_path="/static", static_folder="../frontend/static")

app.config.from_object(Config)
app.url_map.strict_slashes = False
CORS(app)

# ✅ API-Keys aus Umgebungsvariablen lesen
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TREFLE_API_KEY = os.getenv("TREFLE_API_KEY")

db.init_app(app)

# ✅ API-Routen registrieren
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(weather_bp, url_prefix="/weather")
app.register_blueprint(explore_bp, url_prefix="/explore")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend läuft erfolgreich!"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
