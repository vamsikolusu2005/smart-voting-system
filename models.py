# models.py
from flask_sqlalchemy import SQLAlchemy
from app import db

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aadhar = db.Column(db.String(20), unique=True, nullable=False)
    voter_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voter.id'))
    otp = db.Column(db.String(6))
    expires_at = db.Column(db.DateTime)
    used = db.Column(db.Boolean, default=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voter.id'))
    candidate_id = db.Column(db.Integer)
    voted_at = db.Column(db.DateTime)
    location = db.Column(db.String(255))
