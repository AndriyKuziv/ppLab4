from src.model import Playlist, User, Song
from unittest import TestCase, mock
from undecorated import undecorated
from src.route import create_song, get_song_by_id, update_song_by_id, delete_song_by_id


class TestUsers(TestCase):

    def setUp(self) -> None:
        self.song = Song(
            name='name',
            artist='artist'
        )

        self.song_json_create = {
            'name': 'name',
            'artist': 'artist'
        }

        self.get_song_json = {
            'id': None,
            'name': 'name',
            'artist': 'artist'
        }

        self.update_song_json = {
            'name': 'new_name'
        }

    @mock.patch('src.model.playlist.Playlist.save_to_db')
    @mock.patch('src.model.user.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_song(self, mock_request_parser, mock_get_by_username,
                             mock_save_to_db):

        mock_request_parser.return_value = self.song_json_create
        mock_get_by_username.return_value = User()
        mock_save_to_db.return_value = True
        undecorated_get_song = undecorated(create_song)
        result = undecorated_get_song()

        self.assertEqual(({'message': 'Song was successfully created'}, 200), result)

    @mock.patch('src.model.song.Song.get_by_id')
    def test_get_song_by_id(self, mock_get_song_by_id):
        mock_get_song_by_id.return_value = self.song

        undecorated_get_song_by_id = undecorated(get_song_by_id)
        result = undecorated_get_song_by_id(1)

        self.assertEqual(self.get_song_json, result)

    @mock.patch('src.model.playlist.Playlist.get_by_id')
    def test_get_song_by_id_fail(self, mock_get_song_by_id):
        mock_get_song_by_id.return_value = None

        undecorated_get_song_by_id = undecorated(get_song_by_id)
        result = undecorated_get_song_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Song with such id does not exist.',
                                       'source': "Field 'SongId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.model.playlist.Playlist.delete_by_id')
    def test_delete_song_by_id(self, mock_delete_by_id):
        mock_delete_by_id.return_value = self.get_song_json

        undecorated_delete_song_by_id = undecorated(delete_song_by_id)
        result = undecorated_delete_song_by_id(1)

        self.assertEqual(self.get_song_json, result)
