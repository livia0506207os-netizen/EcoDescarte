import json
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup   # CORRETO: importar daqui

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ecodescarte'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------------------
# MODELOS
# ------------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Local(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    local_id = db.Column(db.Integer, db.ForeignKey('local.id'), nullable=False)
    local = db.relationship('Local', backref=db.backref('agendamentos', lazy=True))

# ------------------------
# ROTAS PRINCIPAIS
# ------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        novo_usuario = Usuario(
            nome=request.form['nome'],
            email=request.form['email'],
            senha=request.form['senha']
        )
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/agendamento', methods=['GET','POST'])
def agendamento():
    locais = Local.query.all()
    locais_json = json.dumps([{
        "id": l.id,
        "nome": l.nome,
        "endereco": l.endereco,
        "latitude": l.latitude,
        "longitude": l.longitude
    } for l in locais])
    if request.method == 'POST':
        novo_agendamento = Agendamento(
            nome=request.form['nome'],
            email=request.form['email'],
            data=request.form['data'],
            local_id=request.form['local']
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('agendamento.html', locais=locais, locais_json=Markup(locais_json))

@app.route('/mapa')
def mapa():
    locais = Local.query.all()
    locais_json = json.dumps([{
        "id": l.id,
        "nome": l.nome,
        "endereco": l.endereco,
        "latitude": l.latitude,
        "longitude": l.longitude
    } for l in locais])
    return render_template('mapa.html', locais_json=Markup(locais_json))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email, senha=senha).first()
        if usuario:
            return redirect(url_for('index'))
        else:
            return "Login inválido"
    return render_template('login.html')

@app.route('/saibamais')
def saibamais():
    return render_template('saibamais.html')

@app.route('/admin/locais', methods=['GET','POST'])
def admin_locais():
    if request.method == 'POST':
        novo_local = Local(
            nome=request.form['nome'],
            endereco=request.form['endereco'],
            latitude=float(request.form['latitude']) if request.form['latitude'] else None,
            longitude=float(request.form['longitude']) if request.form['longitude'] else None
        )
        db.session.add(novo_local)
        db.session.commit()
        return redirect(url_for('admin_locais'))
    locais = Local.query.all()
    return render_template('admin_locais.html', locais=locais)

# ------------------------
# CRIAR BANCO
# ------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




