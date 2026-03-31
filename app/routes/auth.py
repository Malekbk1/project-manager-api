from flask import blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db 
from app.models import user 


auth_bp = blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "username, email, and password are required"}), 400
    
    if user.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409
    
    if user.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already taken"}), 409
    
    user = user(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)    
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "email and password are required"}), 400
    
    user = user.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401
    
    token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Login successful", "token": token, "user": user.to_dict()}), 200