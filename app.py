from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Conexão com o banco PostgreSQL do Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos
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

# Lista de ecopontos reais de Limeira
ECOPOINTS = [
    {"nome": "Ecoponto Anavec", "endereco": "Rua Prof. Otávio Pimenta Reis – Jd. Anavec", "latitude": -22.5695, "longitude": -47.4012},
    {"nome": "Ecoponto Santa Eulália", "endereco": "Av. Dr. Antônio Prince de Oliveira – Jd. Santa Eulália", "latitude": -22.5638, "longitude": -47.4087},
    {"nome": "Ecoponto Lagoa Nova", "endereco": "Av. Dr. Antônio de Luna – Jd. Lagoa Nova", "latitude": -22.5559, "longitude": -47.4143}
]

# Rotas
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro_usuario", methods=["GET", "POST"])
def cadastro_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        novo_usuario = Usuario(nome=nome, email=email)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("cadastro_usuario.html")

@app.route("/agendar_coleta", methods=["GET", "POST"])
def agendar_coleta():
    usuarios = Usuario.query.all()
    if request.method == "POST":
        usuario_id = request.form["usuario_id"]
        tipo = request.form["tipo"]
        data = request.form["data"]
        local = request.form["local"]
        novo_agendamento = Agendamento(tipo=tipo, data=data, local=local, usuario_id=usuario_id)
        db.session.add(novo_agendamento)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("agendar_coleta.html", usuarios=usuarios, locais=ECOPOINTS)

@app.route("/admin/agendamentos")
def listar_agendamentos():
    usuarios = Usuario.query.all()
    agendamentos = Agendamento.query.all()
    return render_template("listar_agendamentos.html", usuarios=usuarios, agendamentos=agendamentos)

@app.route("/mapa")
def mapa():
    # Passa a lista de ecopontos para o template
    return render_template("mapa.html", locais=ECOPOINTS)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)





















