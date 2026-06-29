from flask import Blueprint, jsonify, request

from repositories.employees import (
    create_agent,
    delete_agent,
    get_agent_by_id,
    get_all_agents,
    update_agent,
)
from routes.auth import login_required


agents_bp = Blueprint("agents", __name__)


def normalize_optional_int(value):
    if value in ("", None, "null", "None"):
        return None
    return int(value)


@agents_bp.route("/agents", methods=["GET"])
@login_required
def list_agents():
    return jsonify(get_all_agents()), 200


@agents_bp.route("/agents/<int:agent_id>", methods=["GET"])
@login_required
def get_agent(agent_id):
    agent = get_agent_by_id(agent_id)

    if not agent:
        return jsonify({"error": "Agent not found"}), 404

    return jsonify(agent), 200


@agents_bp.route("/agents", methods=["POST"])
@login_required
def add_agent():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    specialization = data.get("specialization", "").strip()
    status = data.get("status", "Active").strip()
    location_id = normalize_optional_int(data.get("location_id"))

    if not name or not email:
        return jsonify({"error": "Agent name and email are required"}), 400

    agent = create_agent(
        name=name,
        email=email,
        phone=phone,
        specialization=specialization,
        location_id=location_id,
        status=status,
    )

    if not agent:
        return jsonify({"error": "Agent email already exists"}), 409

    return jsonify({
        "message": "Agent created successfully",
        "agent": agent
    }), 201


@agents_bp.route("/agents/<int:agent_id>", methods=["PUT"])
@login_required
def edit_agent(agent_id):
    existing = get_agent_by_id(agent_id)

    if not existing:
        return jsonify({"error": "Agent not found"}), 404

    data = request.get_json(silent=True) or {}

    name = data.get("name", existing["name"]).strip()
    email = data.get("email", existing["email"]).strip()
    phone = data.get("phone", existing.get("phone") or "").strip()
    specialization = data.get("specialization", existing.get("specialization") or "").strip()
    status = data.get("status", existing["status"]).strip()
    location_id = normalize_optional_int(data.get("location_id", existing.get("location_id")))

    agent = update_agent(
        agent_id=agent_id,
        name=name,
        email=email,
        phone=phone,
        specialization=specialization,
        location_id=location_id,
        status=status,
    )

    if not agent:
        return jsonify({"error": "Agent email already exists"}), 409

    return jsonify({
        "message": "Agent updated successfully",
        "agent": agent
    }), 200


@agents_bp.route("/agents/<int:agent_id>", methods=["DELETE"])
@login_required
def remove_agent(agent_id):
    deleted = delete_agent(agent_id)

    if not deleted:
        return jsonify({"error": "Agent not found"}), 404

    return jsonify({"message": "Agent deleted successfully"}), 200
