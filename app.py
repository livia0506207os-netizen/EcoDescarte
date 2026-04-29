import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "chave-secreta"

# Configuração do banco (Render usa DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------- MODELOS -----------------
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
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# ----------------- ROTAS -----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = generate_password_hash(request.form["senha"])
        usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session["usuario_id"] = usuario.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("index"))
        else:
            flash("Email ou senha inválidos", "danger")
    return render_template("login.html")

@app.route("/agendamento", methods=["GET", "POST"])
def agendamento():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        data = request.form["data"]
        local = request.form["local"]
        agendamento = Agendamento(nome=nome, email=email, data=data, local=local)
        db.session.add(agendamento)
        db.session.commit()
        flash("Agendamento realizado com sucesso!", "success")
        return redirect(url_for("index"))
    locais = Local.query.all()
    return render_template("agendamento.html", locais=locais)

@app.route("/admin/locais")
def admin_locais():
    locais = Local.query.all()
    return render_template("admin_locais.html", locais=locais)

@app.route("/admin/agendamentos")
def admin_agendamentos():
    agendamentos = Agendamento.query.all()
    return render_template("admin_agendamentos.html", agendamentos=agendamentos)

@app.route("/admin/usuarios")
def admin_usuarios():
    usuarios = Usuario.query.all()
    return render_template("admin_usuarios.html", usuarios=usuarios)

@app.route("/saibamais")
def saibamais():
    return render_template("saibamais.html")

if __name__ == "__main__":
    app.run(debug=True)
