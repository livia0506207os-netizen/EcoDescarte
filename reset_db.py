from app import db, app

with app.app_context():
    db.drop_all()   # apaga todas as tabelas
    db.create_all() # recria com os modelos atuais
    print("Banco resetado e recriado com sucesso!")
