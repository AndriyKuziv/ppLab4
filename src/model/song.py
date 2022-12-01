from src.app import db
from strenum import StrEnum
from sqlalchemy import Enum
from src.error_handler.exception_wrapper import handle_error_format
from src.error_handler.exception_wrapper import handle_server_exception


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    artist = db.Column(db.String(255), unique=False, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, song_id):
        return cls.query.filter_by(id=song_id).first()

    @classmethod
    def get_by_name(cls, song_name):
        return cls.query.filter_by(name=song_name).first()

    @classmethod
    def delete_by_id(cls, playlist_id):
        song = Song.get_by_id(playlist_id)

        if not song:
            return handle_error_format('Song with such id does not exist.',
                                       'Field \'SongId\' in path parameters.'), 404

        song_json = Song.to_json(song)

        cls.query.filter_by(id=playlist_id).delete()
        db.session.commit()

        return song_json
