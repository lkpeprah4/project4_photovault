from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")
    photos = db.relationship("Photo", backref="owner", lazy=True)


class Photo(db.Model):
    __tablename__ = "photos"
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(80),nullable=False)
    description=db.Column(db.String(120))
    image_url=db.Column(db.String(500),nullable=False)
    visibility=db.Column(db.String(30), default="private")
    user_id=db.Column(db.Integer(), db.ForeignKey("users.id") , nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)