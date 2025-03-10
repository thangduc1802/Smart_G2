from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    plants = db.relationship('Plant')

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sunlight = db.Column(db.String(50))
    water = db.Column(db.String(50))
    soil = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)