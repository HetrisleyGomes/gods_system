from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))

    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'))
    fichas = db.relationship('Ficha', backref='usuario', lazy=True)
