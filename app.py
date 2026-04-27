from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    # Render usa postgres://, mas SQLAlchemy espera postgresql+pg8000://
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

@app.route("/agendamento")
def agendamento():
    return render_template("agendamento.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/saibamais")
def saibamais():
    return render_template("saibamais.html")

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
        novo_agendamento = Agendamento(usuario_id=usuario_id, tipo=tipo, data=data, local=local)
        db.session.add(novo_agendamento)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("agendar_coleta.html", usuarios=usuarios, locais=ECOPOINTS)

@app.route("/admin/agendamentos")
def listar_agendamentos():
    usuarios = Usuario.query.all()
    agendamentos = Agendamento.query.all()
    return render_template("listar_agendamentos.html", usuarios=usuarios, agendamentos=agendamentos)

@app.route("/admin/usuarios")
def admin_usuarios():
    usuarios = Usuario.query.all()
    return render_template("admin_usuarios.html", usuarios=usuarios)

@app.route("/admin/locais")
def admin_locais():
    return render_template("admin_locais.html", locais=ECOPOINTS)

# ------------------------
# MAIN
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
