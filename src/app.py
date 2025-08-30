from flask import Flask, redirect, url_for
from src.db import init_app as init_db
from src.routes import bp as api_bp
from src.ui import bp as ui_bp
import os

def create_app() -> Flask:
    app = Flask(__name__)
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL no está definida")
    app.config["DATABASE_URL"] = db_url

    init_db(app)
    app.register_blueprint(api_bp)
    app.register_blueprint(ui_bp)

    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    @app.get("/") 
    def root():
        return redirect(url_for("ui.index"))

    return app

app = create_app()
