from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/admin_locais")
def admin_locais():
    return render_template("admin_locais.html")

@app.route("/admin_agendamentos")
def admin_agendamentos():
    return render_template("admin_agendamentos.html")

@app.route("/admin_usuarios")
def admin_usuarios():
    return render_template("admin_usuarios.html")

@app.route("/editar_agendamento")
def editar_agendamento():
    return render_template("editar_agendamento.html")

@app.route("/editar_usuario")
def editar_usuario():
    return render_template("editar_usuario.html")

if __name__ == "__main__":
    app.run(debug=True)







