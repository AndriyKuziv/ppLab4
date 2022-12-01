from src.app import db
from src.model.song import Song
from src.error_handler.exception_wrapper import handle_error_format
from src.error_handler.exception_wrapper import handle_server_exception


class PlaylistSong(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    playlist_id = db.Column(db.Integer(), db.ForeignKey('playlist.id', ondelete='CASCADE'))
    song_id = db.Column(db.Integer(), db.ForeignKey('song.id', ondelete='CASCADE'))

    def to_json(self):
        return {
            'id': self.id,
            'playlist_id': self.playlist_id,
            'song_id': self.song_id
        }

    @classmethod
    def return_all_by_playlist_id(cls, playlistId):
        def to_json(song):
            return {
                'name': song.name,
                'artist': song.artist
            }

        res = [to_json(song) for song in db.session.query(
            Song
        ).join(
            PlaylistSong, PlaylistSong.song_id == Song.id
        ).filter_by(playlist_id=playlistId)]
        return res

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, playlistsong_id):
        return cls.query.filter_by(id=playlistsong_id).first()

    @classmethod
    def get_by_song_id_and_playlist_id(cls, song_id, playlist_id):
        return cls.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()

    @classmethod
    def delete_by_song_id_and_playlist_id(cls, song_id, playlist_id):
        playlistsong = PlaylistSong.get_by_song_id_and_playlist_id(song_id, playlist_id)

        if not playlistsong:
            return handle_error_format('Playlist with such id does not exist',
                                       'Field \'SongId\' in path parameters.'), 404

        playlistsong_json = PlaylistSong.to_json(playlistsong)
        cls.query.filter_by(playlist_id=playlist_id, song_id=song_id).delete()
        db.session.commit()

        return playlistsong_json

    @classmethod
    def delete_by_id(cls, playlistsong_id):
        playlistsong = PlaylistSong.get_by_id(playlistsong_id)

        if not playlistsong:
            return handle_error_format('Record with such id does not exist.',
                                       'Field \'recordId\' in path parameters.'), 404

        playlistsong_json = PlaylistSong.to_json(playlistsong)

        cls.query.filter_by(id=playlistsong_id).delete()
        db.session.commit()

        return playlistsong_json
