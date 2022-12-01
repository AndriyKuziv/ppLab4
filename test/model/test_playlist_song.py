from unittest import TestCase, mock
from src.model import Playlist, PlaylistSong


class TestPlaylistSong(TestCase):

    def setUp(self) -> None:
        self.playlistsong = PlaylistSong(
            song_id=1,
            playlist_id=1
        )

    def test_to_json(self):
        playlistsong = self.playlistsong

        expected_json = {'id': None,
                         'song_id': 1,
                         'playlist_id': 1
                         }

        result = playlistsong.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        playlistsong = self.playlistsong

        mock_add.return_value = None
        mock_commit.return_value = None

        PlaylistSong.save_to_db(playlistsong)

        mock_add.assert_called_once_with(playlistsong)
        mock_commit.assert_called_once_with()

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        playlistsong = self.playlistsong
        playlistsong.id = 1
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = playlistsong

        result = Playlist.get_by_id(1)

        self.assertEqual(playlistsong, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.model.playlist.Playlist.get_by_id')
    def test_delete_by_id(self, mock_get_by_id, mock_query_property_getter, mock_commit):
        mock_get_by_id.return_value = self.playlistsong
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = PlaylistSong.delete_by_id('id')

        self.assertTrue(result)
