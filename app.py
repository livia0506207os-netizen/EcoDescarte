from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuração do banco (Render fornece DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "segredo_local")
db = SQLAlchemy(app)

# ------------------------
# MODELOS
# ------------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    local = db.Column(db.String(100), nullable=False)

# ------------------------
# ROTAS PRINCIPAIS
# ------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/saibamais")
def saibamais():
    return render_template("saibamais.html")

# ------------------------
# CADASTRO / LOGIN
# ------------------------
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        flash("Usuário cadastrado com sucesso!")
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
            flash("Login realizado com sucesso!")
            return redirect(url_for("index"))
        else:
            flash("Email ou senha inválidos.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    flash("Logout realizado.")
    return redirect(url_for("index"))

# ------------------------
# AGENDAMENTO
# ------------------------
@app.route("/agendamento", methods=["GET", "POST"])
def agendamento():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        data = request.form["data"]
        local = request.form["local"]

        novo_agendamento = Agendamento(nome=nome, email=email, data=data, local=local)
        db.session.add(novo_agendamento)
        db.session.commit()

        flash("Agendamento realizado com sucesso!")
        return redirect(url_for("index"))

    return render_template("agendamento.html")

# ------------------------
# ADMIN
# ------------------------
@app.route("/admin/usuarios")
def admin_usuarios():
    usuarios = Usuario.query.all()
    return render_template("admin_usuarios.html", usuarios=usuarios)

@app.route("/admin/agendamentos")
def admin_agendamentos():
    agendamentos = Agendamento.query.all()
    return render_template("admin_agendamentos.html", agendamentos=agendamentos)

# ------------------------
# INICIALIZAÇÃO
# ------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
