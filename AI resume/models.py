from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user') # 'user' or 'admin'
    resumes = db.relationship('Resume', backref='user', lazy=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float, nullable=True) # Overall resume score (0-100)
    feedback_missing = db.Column(db.Text, nullable=True)
    feedback_weak = db.Column(db.Text, nullable=True)
    feedback_strong = db.Column(db.Text, nullable=True)
    extracted_skills = db.Column(db.Text, nullable=True) # comma separated skills
    job_match_score = db.Column(db.Float, nullable=True)
