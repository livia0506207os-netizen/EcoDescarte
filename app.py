from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os, json

app = Flask(__name__)
app.secret_key = "segredo-super-seguro"

# Configuração do banco
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+pg8000://")
else:
    db_url = "sqlite:///local.db"

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    local = db.Column(db.String(100), nullable=False)

class Local(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.String(50), nullable=True)
    longitude = db.Column(db.String(50), nullable=True)

with app.app_context():
    db.create_all()

# Rotas
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/saibamais")
def saibamais():
    return render_template("saibamais.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = Usuario.query.filter_by(email=email, senha=senha).first()
        if usuario:
            session["usuario_id"] = usuario.id
            return redirect(url_for("index"))
        else:
            return "Login inválido"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    return redirect(url_for("index"))

@app.route("/agendamento", methods=["GET", "POST"])
def agendamento():
    locais = Local.query.all()
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        data = request.form["data"]
        local = request.form["local"]

        novo_agendamento = Agendamento(nome=nome, email=email, data=data, local=local)
        db.session.add(novo_agendamento)
        db.session.commit()
        return redirect(url_for("index"))

    locais_json = json.dumps([{
        "nome": l.nome,
        "endereco": l.endereco,
        "latitude": l.latitude,
        "longitude": l.longitude
    } for l in locais]) if locais else "[]"

    return render_template("agendamento.html", locais=locais, locais_json=locais_json)

@app.route("/admin/locais", methods=["GET", "POST"])
def admin_locais():
    if request.method == "POST":
        nome = request.form["nome"]
        endereco = request.form["endereco"]
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        novo_local = Local(nome=nome, endereco=endereco, latitude=latitude, longitude=longitude)
        db.session.add(novo_local)
        db.session.commit()
        return redirect(url_for("admin_locais"))

    locais = Local.query.all()
    usuarios = Usuario.query.all()
    agendamentos = Agendamento.query.all()
    return render_template("admin_locais.html", locais=locais, usuarios=usuarios, agendamentos=agendamentos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
