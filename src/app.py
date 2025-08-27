from flask import Flask
from config import DevelopmentConfig
from db import mysql
from routes import consumidores_bp, tecnicos_bp, administradores_bp
from ui import ui as ui_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

mysql.init_app(app)

app.register_blueprint(consumidores_bp)
app.register_blueprint(tecnicos_bp)
app.register_blueprint(administradores_bp)
app.register_blueprint(ui_bp)
