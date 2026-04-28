from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os, json

app = Flask(__name__)

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
    agendamentos = db.relationship("Agendamento", backref="usuario", lazy=True)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    local = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

class Local(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))

# Rotas públicas
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/saibamais")
def saibamais():
    return render_template("saibamais.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

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

@app.route("/agendamento", methods=["GET", "POST"])
def agendamento():
    locais = Local.query.all()
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        data = request.form["data"]
        local = request.form["local"]

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            usuario = Usuario(nome=nome, email=email)
            db.session.add(usuario)
            db.session.commit()

        novo_agendamento = Agendamento(
            usuario_id=usuario.id,
            tipo="Eletrônicos",
            data=data,
            local=local
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("agendamento.html",
        locais=locais,
        locais_json=json.dumps([{
            "nome": l.nome,
            "endereco": l.endereco,
            "latitude": l.latitude,
            "longitude": l.longitude
        } for l in locais])
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        # Aqui você faria a validação
        return redirect(url_for("index"))
    return render_template("login.html")

# Admin locais
@app.route("/admin/locais", methods=["GET", "POST"])
def admin_locais():
    if request.method == "POST":
        nome = request.form["nome"]
        endereco = request.form["endereco"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        novo_local = Local(nome=nome, endereco=endereco, latitude=latitude, longitude=longitude)
        db.session.add(novo_local)
        db.session.commit()
        return redirect(url_for("admin_locais"))
    locais = Local.query.all()
    return render_template("admin_locais.html", locais=locais)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
