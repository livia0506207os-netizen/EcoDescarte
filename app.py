from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    agendamentos = db.relationship("Agendamento", backref="usuario", lazy=True)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    local = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

ECOPOINTS = [
    {"nome": "Ecoponto Anavec", "endereco": "Rua Prof. Otávio Pimenta Reis – Jd. Anavec", "latitude": -22.5695, "longitude": -47.4012},
    {"nome": "Ecoponto Santa Eulália", "endereco": "Av. Dr. Antônio Prince de Oliveira – Jd. Santa Eulália", "latitude": -22.5638, "longitude": -47.4087},
    {"nome": "Ecoponto Lagoa Nova", "endereco": "Av. Dr. Antônio de Luna – Jd. Lagoa Nova", "latitude": -22.5559, "longitude": -47.4143}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mapa")
def mapa():
    return render_template("mapa.html", locais=ECOPOINTS)

# demais rotas...
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
