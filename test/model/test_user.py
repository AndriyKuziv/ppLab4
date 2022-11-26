from unittest import TestCase, mock
from src.model import User, Playlist


class TestUser(TestCase):
    def setUp(self) -> None:
        self.user = User(
            username='username',
            email='email@gmail.com',
            password='password'
        )

    def test_to_json(self):
        user = self.user

        expected_json = {'email': 'email@gmail.com',
                         'id': None,
                         'username': 'username',
                         'password': 'password',
                         'roles': []
                         }

        result = user.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        user = self.user

        mock_add.return_value = None
        mock_commit.return_value = None

        User.save_to_db(user)

        mock_add.assert_called_once_with(user)
        mock_commit.assert_called_once_with()

    # def test_save_to_db(self, mock_add, mock_commit):
    #     user = self.user
    #
    #     mock_add.return_value = None
    #     mock_commit.return_value = None
    #
    #     User.save_to_db(user)
    #
    #     mock_add.assert_called_once_with(user)
    #     mock_commit.assert_called_once_with()

    def test_generate_hash(self):
        user = self.user

        result = user.generate_hash('password')

        self.assertTrue(result)

    def test_verify_hash(self):
        user = self.user
        user.password = user.generate_hash(user.password)
        result = user.verify_hash('password', user.password)

        self.assertTrue(result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_username(self, mock_query_property_getter):
        user = self.user
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = user
        result = User.get_by_username('username')

        self.assertEqual(user, result)
