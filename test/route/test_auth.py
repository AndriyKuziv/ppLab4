# from unittest import TestCase, mock
# from src.model import User, Role
# from undecorated import undecorated
# from src.model.user import get_user_roles, Role
#
#
# class TestAuth(TestCase):
#
#     def setUp(self) -> None:
#         self.user = User(
#             username='username',
#             email='email@gmail.com',
#             password='password'
#         )
#
#         self.user.roles.append(Role(id=1, name='user'))
#         self.user.roles.append(Role(id=2, name='admin'))
#
#     @mock.patch('src.main.User.check_hash')
#     @mock.patch('src.main.User.get_by_username')
#     def test_verify_password(self, mock_get_by_username, mock_check_hash):
#         mock_get_by_username.return_value = self.user
#         mock_check_hash.return_value = True
#
#         undecorated_verify_password = undecorated(verify_password)
#         result = undecorated_verify_password('username', 'password')
#
#         self.assertEqual('username', result)
#
#     @mock.patch('src.model.User.get_by_username')
#     def test_get_user_roles(self, mock_get_by_username):
#         mock_get_by_username.return_value = self.user
#
#         undecorated_get_user_roles = undecorated(get_user_roles)
#         result = undecorated_get_user_roles('username')
#
#         self.assertEqual(['user', 'admin'], result)
#
#     def test_hello(self):
#         undecorated_hello = undecorated(hello)
#         result = undecorated_hello()
#
#         self.assertEqual(result, 'Hello World 29')