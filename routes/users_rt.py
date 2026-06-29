from flask import Blueprint, jsonify, request, session

from repositories.users import authenticate_user, create_user, get_user_by_id


users_bp = Blueprint("users", __name__)


@users_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    user = create_user(name=name, email=email, password=password)

    if not user:
        return jsonify({"error": "Email already registered"}), 409

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]

    return jsonify({
        "message": "Registration successful",
        "user": user
    }), 201


@users_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = authenticate_user(email=email, password=password)

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]

    return jsonify({
        "message": "Login successful",
        "user": user
    }), 200


@users_bp.route("/logout", methods=["POST"])
def logout_user():
    session.clear()
    return jsonify({"message": "Logout successful"}), 200


@users_bp.route("/session", methods=["GET"])
def get_session():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"authenticated": False}), 401

    user = get_user_by_id(user_id)

    if not user:
        session.clear()
        return jsonify({"authenticated": False}), 401

    return jsonify({
        "authenticated": True,
        "user": user
    }), 200
