from db import db

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registry = db.Column(db.String(7), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
