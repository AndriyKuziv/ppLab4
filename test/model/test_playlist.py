from unittest import TestCase, mock
from src.model import Playlist


class TestPlaylist(TestCase):

    def setUp(self) -> None:
        self.playlist = Playlist(
            name='PlaylistName',
            state='Public'
        )

    def test_to_json(self):
        playlist = self.playlist

        expected_json = {'id': None,
                         'name': 'PlaylistName',
                         'user_id': None,
                         'state': 'Public'
                         }

        result = playlist.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        playlist = self.playlist

        mock_add.return_value = None
        mock_commit.return_value = None

        Playlist.save_to_db(playlist)

        mock_add.assert_called_once_with(playlist)
        mock_commit.assert_called_once_with()

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_name(self, mock_query_property_getter):
        playlist = self.playlist
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = playlist

        result = playlist.get_by_name('PlaylistName')

        self.assertEqual(playlist, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        playlist = self.playlist
        playlist.id = 1
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = playlist

        result = Playlist.get_by_id(1)

        self.assertEqual(playlist, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.model.playlist.Playlist.get_by_id')
    def test_delete_by_id(self, mock_get_by_id, mock_query_property_getter, mock_commit):
        mock_get_by_id.return_value = self.playlist
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = Playlist.delete_by_id('id')

        self.assertTrue(result)

    @mock.patch('src.model.playlist.Playlist.get_by_id')
    def test_delete_by_identifier_with_invalid_user(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result = Playlist.delete_by_id('id')

        self.assertEqual(({'errors': [{'message': 'Playlist with such id does not exist.',
              'source': "Field 'PlaylistId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)
