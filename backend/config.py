import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///smart-garden.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "mein-geheimer-schlüssel")