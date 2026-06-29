import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from db import get_database_path
from routes.users_rt import users_bp
from routes.assets_rt import listings_bp
from routes.employees_rt import agents_bp
from routes.locations_rt import locations_bp
from routes.dashboard_rt import dashboard_bp


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", static_url_path="")

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "real-estate-operations-dashboard-dev-secret"
    )
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    CORS(app, supports_credentials=True)

    app.register_blueprint(users_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(agents_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "login.html")

    @app.route("/health")
    def health():
        return jsonify({
            "status": "ok",
            "message": "Real Estate Operations Dashboard API is running"
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()


if __name__ == "__main__":
    print(f"Using database at: {get_database_path()}")
    print("✅ Real Estate Operations Dashboard running locally at http://127.0.0.1:5000/")
    app.run(debug=True)
