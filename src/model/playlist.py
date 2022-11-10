from src.app import db
from strenum import StrEnum
from sqlalchemy import Enum
from src.error_handler.exception_wrapper import handle_error_format
from src.error_handler.exception_wrapper import handle_server_exception


class State(StrEnum):
    PUBLIC = 'Public'
    PRIVATE = 'Private'


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    userId = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    state = db.Column(Enum(State), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.userId,
            'state': self.state
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, playlist_id):
        return cls.query.filter_by(id=playlist_id).first()

    @classmethod
    def get_by_name(cls, playlist_name):
        return cls.query.filter_by(name=playlist_name).first()


    @classmethod
    def delete_by_id(cls, playlist_id):
        playlist = Playlist.get_by_id(playlist_id)

        if not playlist:
            return handle_error_format('Playlist with such id does not exist.',
                                       'Field \'PlaylistId\' in path parameters.'), 404

        playlist_json = Playlist.to_json(playlist)

        cls.query.filter_by(id=playlist_id).delete()
        db.session.commit()

        return playlist_json
