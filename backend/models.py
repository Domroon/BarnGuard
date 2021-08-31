from datetime import datetime
from config import db, ma


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(16), unique=False, nullable=False)
    time = db.Column(db.String(8), unique=False, nullable=False)
    thumbnail_photo = db.Column(db.String(120), unique=True, nullable=False)
    videoname = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Video('{self.id}', '{self.date}', '{self.time}', '{self.thumbnail_photo}', '{self.videoname}')"


class VideoSchema(ma.Schema):
    class Meta:
        fields = ("date", "time", "thumbnail_photo", "videoname")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)