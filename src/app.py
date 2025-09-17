from flask import Flask, redirect, request, url_for, jsonify
from flask_cors import CORS
from src.db import init_app as init_db
from src.routes import bp as api_bp
from src.ui import bp as ui_bp
import os

def create_app() -> Flask:
    app = Flask(__name__)

    app.url_map.strict_slashes = False

    CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"])

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL no está definida")
    app.config["DATABASE_URL"] = db_url


    init_db(app)

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(ui_bp)

    @app.get("/ping")
    def ping():
        return jsonify({"status": "ok"}), 200
    
    @app.get("/__routes")
    def routes():
        return {"routes": [str(r) for r in app.url_map.iter_rules()]}

    @app.route("/__echo", methods=["POST"])
    def echo():
        return {"ok": True, "json": (request.get_json(silent=True) or {})}


    @app.get("/")
    def root():
        return redirect(url_for("ui.index"))

    return app

app = create_app()
