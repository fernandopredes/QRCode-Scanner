from db import db

class PatrimonyModel(db.Model):
    __tablename__ = 'patrimony'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    airport = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    responsible = db.Column(db.String(50), nullable=False)
    registry = db.Column(db.String(7), nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
