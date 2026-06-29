from flask import Blueprint, jsonify

from routes.auth import login_required
from services.dashboard import get_dashboard_stats


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard/stats", methods=["GET"])
@login_required
def dashboard_stats():
    return jsonify(get_dashboard_stats()), 200
