from flask import Blueprint, jsonify, request

from repositories.locations import (
    create_location,
    delete_location,
    get_all_locations,
    get_location_by_id,
    update_location,
)
from routes.auth import login_required


locations_bp = Blueprint("locations", __name__)


@locations_bp.route("/locations", methods=["GET"])
@login_required
def list_locations():
    return jsonify(get_all_locations()), 200


@locations_bp.route("/locations/<int:location_id>", methods=["GET"])
@login_required
def get_location(location_id):
    location = get_location_by_id(location_id)

    if not location:
        return jsonify({"error": "Location not found"}), 404

    return jsonify(location), 200


@locations_bp.route("/locations", methods=["POST"])
@login_required
def add_location():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    city = data.get("city", "").strip()
    address = data.get("address", "").strip()
    status = data.get("status", "Active").strip()

    if not name or not city:
        return jsonify({"error": "Location name and city are required"}), 400

    location = create_location(
        name=name,
        city=city,
        address=address,
        status=status,
    )

    return jsonify({
        "message": "Location created successfully",
        "location": location
    }), 201


@locations_bp.route("/locations/<int:location_id>", methods=["PUT"])
@login_required
def edit_location(location_id):
    existing = get_location_by_id(location_id)

    if not existing:
        return jsonify({"error": "Location not found"}), 404

    data = request.get_json(silent=True) or {}

    name = data.get("name", existing["name"]).strip()
    city = data.get("city", existing["city"]).strip()
    address = data.get("address", existing.get("address") or "").strip()
    status = data.get("status", existing["status"]).strip()

    location = update_location(
        location_id=location_id,
        name=name,
        city=city,
        address=address,
        status=status,
    )

    return jsonify({
        "message": "Location updated successfully",
        "location": location
    }), 200


@locations_bp.route("/locations/<int:location_id>", methods=["DELETE"])
@login_required
def remove_location(location_id):
    deleted = delete_location(location_id)

    if not deleted:
        return jsonify({"error": "Location not found"}), 404

    return jsonify({"message": "Location deleted successfully"}), 200
