from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patrimony(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    airport = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    responsible = db.Column(db.String(50), nullable=False)
