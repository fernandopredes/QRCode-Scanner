from db import db
from datetime import datetime

class ScannedPatrimony(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patrimony_id = db.Column(db.Integer, db.ForeignKey('patrimony.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('UserModel', backref=db.backref('scanned_patrimonies', lazy=True))
    patrimony = db.relationship('PatrimonyModel', backref=db.backref('scanned_by_users', lazy=True))
