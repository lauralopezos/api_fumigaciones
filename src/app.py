import os
from flask import Flask
from db import init_app as init_db
from routes import bp as api_bp
from ui import bp as ui_bp

def create_app() -> Flask:
    app = Flask(__name__)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL no está definida. Configúrala en tu entorno "
            "(o usa DATABASE_URL_TEST en CI y conftest la copiará)."
        )
    app.config["DATABASE_URL"] = db_url

    init_db(app)
    app.register_blueprint(api_bp) 
    app.register_blueprint(ui_bp)   

    @app.route("/ping")
    def ping():
        return {"status": "ok"}

    return app

app = create_app()
