from src.app import db
from strenum import StrEnum
from sqlalchemy import Enum


class State(StrEnum):
    PUBLIC = 'Public'
    PRIVATE = 'Private'


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    state = db.Column(Enum(State), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()