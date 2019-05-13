import mock
import unittest

from app.models.user import User, Role


class UserEntityTest(unittest.TestCase):

    def test_role_str_method_should_return_role_name(self):
        role_name = "exRoleName"

        mock_role = mock.Mock(spec=Role)
        mock_role.name = role_name

        self.assertEqual(Role.__str__(mock_role), role_name)

    def test_user_str_method_should_return_username(self):
        role_name = "exRoleName"

        username = "example_username"
        name = "ExName"
        surname = "ExLAstName"
        email = "example@mail.ru"
        phone = "+9960000000000000"

        mock_role = mock.Mock(spec=Role)
        mock_role.name = role_name

        mock_instance = mock.Mock(spec=User)
        conf = {
            'username': username,
            'name': name,
            'surname': surname,
            'email': email,
            'phone': phone
        }

        mock_instance.configure_mock(**conf)

        self.assertEqual(User.__str__(mock_instance), username)
