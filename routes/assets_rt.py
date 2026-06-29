from flask import Blueprint, jsonify, request

from repositories.assets import (
    create_listing,
    delete_listing,
    get_all_listings,
    get_listing_by_id,
    update_listing,
)
from routes.auth import login_required


listings_bp = Blueprint("listings", __name__)


def normalize_optional_int(value):
    if value in ("", None, "null", "None"):
        return None
    return int(value)


def normalize_int(value, default=0):
    if value in ("", None, "null", "None"):
        return default
    return int(value)


def normalize_float(value, default=0.0):
    if value in ("", None, "null", "None"):
        return default
    return float(value)


@listings_bp.route("/listings", methods=["GET"])
@login_required
def list_listings():
    return jsonify(get_all_listings()), 200


@listings_bp.route("/listings/<int:listing_id>", methods=["GET"])
@login_required
def get_listing(listing_id):
    listing = get_listing_by_id(listing_id)

    if not listing:
        return jsonify({"error": "Listing not found"}), 404

    return jsonify(listing), 200


@listings_bp.route("/listings", methods=["POST"])
@login_required
def add_listing():
    data = request.get_json(silent=True) or {}

    title = data.get("title", "").strip()
    address = data.get("address", "").strip()
    city = data.get("city", "").strip()
    property_type = data.get("property_type", "").strip()
    price = normalize_float(data.get("price"))
    bedrooms = normalize_int(data.get("bedrooms"))
    bathrooms = normalize_int(data.get("bathrooms"))
    status = data.get("status", "Available").strip()
    description = data.get("description", "").strip()
    agent_id = normalize_optional_int(data.get("agent_id"))
    location_id = normalize_optional_int(data.get("location_id"))

    if not title or not address or not city or not property_type:
        return jsonify({"error": "Title, address, city, and property type are required"}), 400

    if price <= 0:
        return jsonify({"error": "Price/rent must be greater than 0"}), 400

    listing = create_listing(
        title=title, address=address, city=city, property_type=property_type,
        price=price, bedrooms=bedrooms, bathrooms=bathrooms, status=status,
        description=description, agent_id=agent_id, location_id=location_id,
    )

    return jsonify({"message": "Listing created successfully", "listing": listing}), 201


@listings_bp.route("/listings/<int:listing_id>", methods=["PUT"])
@login_required
def edit_listing(listing_id):
    existing = get_listing_by_id(listing_id)

    if not existing:
        return jsonify({"error": "Listing not found"}), 404

    data = request.get_json(silent=True) or {}

    listing = update_listing(
        listing_id=listing_id,
        title=data.get("title", existing["title"]).strip(),
        address=data.get("address", existing["address"]).strip(),
        city=data.get("city", existing["city"]).strip(),
        property_type=data.get("property_type", existing["property_type"]).strip(),
        price=normalize_float(data.get("price", existing["price"])),
        bedrooms=normalize_int(data.get("bedrooms", existing["bedrooms"])),
        bathrooms=normalize_int(data.get("bathrooms", existing["bathrooms"])),
        status=data.get("status", existing["status"]).strip(),
        description=data.get("description", existing.get("description") or "").strip(),
        agent_id=normalize_optional_int(data.get("agent_id", existing.get("agent_id"))),
        location_id=normalize_optional_int(data.get("location_id", existing.get("location_id"))),
    )

    return jsonify({"message": "Listing updated successfully", "listing": listing}), 200


@listings_bp.route("/listings/<int:listing_id>", methods=["DELETE"])
@login_required
def remove_listing(listing_id):
    deleted = delete_listing(listing_id)

    if not deleted:
        return jsonify({"error": "Listing not found"}), 404

    return jsonify({"message": "Listing deleted successfully"}), 200


@listings_bp.route("/listings/<int:listing_id>/show-sheet", methods=["GET"])
@login_required
def generate_show_sheet(listing_id):
    listing = get_listing_by_id(listing_id)

    if not listing:
        return jsonify({"error": "Listing not found"}), 404

    show_sheet = {
        "headline": listing["title"],
        "address": f"{listing['address']}, {listing['city']}",
        "price": listing["price"],
        "property_type": listing["property_type"],
        "bedrooms": listing["bedrooms"],
        "bathrooms": listing["bathrooms"],
        "status": listing["status"],
        "assigned_agent": listing.get("agent_name") or "Unassigned",
        "agent_email": listing.get("agent_email") or "",
        "agent_phone": listing.get("agent_phone") or "",
        "office": listing.get("location_name") or "Not assigned",
        "description": listing.get("description") or "No description available.",
        "marketing_summary": (
            f"{listing['title']} located at {listing['address']}, {listing['city']}. "
            f"This {listing['property_type'].lower()} offers "
            f"{listing['bedrooms']} bedroom(s), {listing['bathrooms']} bathroom(s), "
            f"and is currently marked as {listing['status']}."
        ),
    }

    return jsonify(show_sheet), 200
