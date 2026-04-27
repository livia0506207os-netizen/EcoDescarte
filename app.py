from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco usando pg8000
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+pg8000://")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ------------------------
# MODELOS
# ------------------------
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

# ------------------------
# DADOS FIXOS
# ------------------------
ECOPOINTS = [
    {"nome": "Ecoponto Anavec", "endereco": "Rua Prof. Otávio Pimenta Reis – Jd. Anavec", "latitude": -22.5695, "longitude": -47.4012},
    {"nome": "Ecoponto Santa Eulália", "endereco": "Av. Dr. Antônio Prince de Oliveira – Jd. Santa Eulália", "latitude": -22.5638, "longitude": -47.4087},
    {"nome": "Ecoponto Lagoa Nova", "endereco": "Av. Dr. Antônio de Luna – Jd. Lagoa Nova", "latitude": -22.5559, "longitude": -47.4143}
]

# ------------------------
# ROTAS
# ------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mapa")
def mapa():
    return render_template("mapa.html", locais=ECOPOINTS)

# demais rotas iguais...
