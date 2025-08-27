import os
from flask import Flask, jsonify
from config import cnfg
from db import mysql
from routes import consumidores_bp, tecnicos_bp, administradores_bp
from ui import ui

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TPL_DIR  = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TPL_DIR)
app.config.from_object(cnfg['development'])

mysql.init_app(app)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

app.register_blueprint(consumidores_bp)
app.register_blueprint(tecnicos_bp)
app.register_blueprint(administradores_bp)


app.register_blueprint(ui)

if __name__ == "__main__":
    print("\n== RUTAS REGISTRADAS ==")
    print(app.url_map)
    app.run(debug=True)