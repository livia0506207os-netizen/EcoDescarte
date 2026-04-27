from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 🔹 Conexão com o banco PostgreSQL do Render
# A URL vem da variável de ambiente DATABASE_URL configurada no Render Dashboard
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 🔹 Exemplo de tabela (você pode criar outras conforme precisar)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# 🔹 Rotas principais
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/agendamento")
def agendamento():
    return render_template("agendamento.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/saibamais")
def saibamais():
    return render_template("saibamais.html")

@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

# 🔹 Área administrativa
@app.route("/admin/locais")
def admin_locais():
    return render_template("admin_locais.html")

@app.route("/admin/agendamentos")
def admin_agendamentos():
    return render_template("admin_agendamentos.html")

@app.route("/admin/usuarios")
def admin_usuarios():
    return render_template("admin_usuarios.html")

# 🔹 Rotas de edição
@app.route("/admin/editar_agendamento")
def editar_agendamento():
    return render_template("editar_agendamento.html")

@app.route("/admin/editar_usuario")
def editar_usuario():
    return render_template("editar_usuario.html")

if __name__ == "__main__":
    # Cria as tabelas automaticamente no banco do Render
    with app.app_context():
        db.create_all()
    app.run(debug=True)













