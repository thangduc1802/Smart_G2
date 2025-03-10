from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  
from .models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth_bp", __name__)  

# ✅ Registration
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Check if email already exists
    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"error": "E-Mail already registered!"}), 400

   # Hash the password
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")

    # Save new user
    new_user = User(email=data["email"], password=hashed_password, zip_code=data["zip_code"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 201

# ✅ Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    # Verify user and password
    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"error": "Invalid email or password!"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "message": "Login successful!"})

# ✅ Protected Route (Test)
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"message": f"Welcome, {user.email}!"})

    # Log out using frontend
