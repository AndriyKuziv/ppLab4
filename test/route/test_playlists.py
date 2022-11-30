from src.model import Playlist, User
from unittest import TestCase, mock
from undecorated import undecorated
from src.route import create_playlist, get_playlist_by_id, update_playlist_by_id, delete_playlist_by_id, create_playlist


class TestUsers(TestCase):

    def setUp(self) -> None:
        self.playlist = Playlist(
            name='PlaylistName',
            state='Public'
        )

        self.playlist_json_create = {
            'name': 'PlaylistName',
            'state': 'Public'
        }

        self.get_playlist_json = {
            'id': None,
            'name': 'PlaylistName',
            'user_id': None,
            'state': 'Public'
        }

        self.update_user_json = {
            'name': 'new_PlaylistName'
        }

    @mock.patch('src.model.playlist.Playlist.save_to_db')
    @mock.patch('src.model.user.User.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_playlist(self, mock_request_parser, mock_get_by_id,
                             mock_save_to_db):

        mock_request_parser.return_value = self.playlist_json_create
        mock_get_by_id.return_value = User()
        mock_save_to_db.return_value = True
        undecorated_get_playlist = undecorated(create_playlist)
        result = undecorated_get_playlist(1)

        self.assertEqual(({'message': 'Playlist was successfully created'}, 200), result)

    @mock.patch('src.model.playlist.Playlist.get_by_id')
    def test_get_playlist_by_id(self, mock_get_playlist_by_id):
        mock_get_playlist_by_id.return_value = self.playlist

        undecorated_get_playlist_by_id = undecorated(get_playlist_by_id)
        result = undecorated_get_playlist_by_id(1)

        self.assertEqual(self.get_playlist_json, result)

    @mock.patch('src.model.playlist.Playlist.get_by_id')
    def test_get_playlist_by_id_fail(self, mock_get_playlist_by_id):
        mock_get_playlist_by_id.return_value = None

        undecorated_get_playlist_by_id = undecorated(get_playlist_by_id)
        result = undecorated_get_playlist_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Playlist with such id does not exist.',
                                       'source': "Field 'playlistId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.model.playlist.Playlist.delete_by_id')
    def test_delete_playlist_by_id(self, mock_delete_by_id):
        mock_delete_by_id.return_value = self.get_playlist_json

        undecorated_delete_playlist_by_id = undecorated(delete_playlist_by_id)
        result = undecorated_delete_playlist_by_id(1)

        self.assertEqual(self.get_playlist_json, result)
