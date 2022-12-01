from unittest import TestCase, mock
from src.model import Song


class TestSong(TestCase):

    def setUp(self) -> None:
        self.song = Song(
            name='name',
            artist='artist'
        )

    def test_to_json(self):
        song = self.song

        expected_json = {'id': None,
                         'name': 'name',
                         'artist': 'artist'
                         }

        result = song.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        song = self.song

        mock_add.return_value = None
        mock_commit.return_value = None

        Song.save_to_db(song)

        mock_add.assert_called_once_with(song)
        mock_commit.assert_called_once_with()

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_name(self, mock_query_property_getter):
        song = self.song
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = song

        result = song.get_by_name('name')

        self.assertEqual(song, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        song = self.song
        song.id = 1
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = song

        result = song.get_by_id(1)

        self.assertEqual(song, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.model.playlist.Playlist.get_by_id')
    def test_delete_by_id(self, mock_get_by_id, mock_query_property_getter, mock_commit):
        mock_get_by_id.return_value = self.song
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = Song.delete_by_id('id')

        self.assertTrue(result)

    @mock.patch('src.model.playlist.Playlist.get_by_id')
    def test_delete_by_identifier_with_invalid_id(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result = Song.delete_by_id('id')

        self.assertEqual(({'errors': [{'message': 'Song with such id does not exist.',
              'source': "Field 'songId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)
