from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    nama = db.Column(db.String(50))
    password = db.Column(db.String(64))
    status = db.Column(db.Integer)