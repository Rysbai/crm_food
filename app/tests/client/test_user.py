import json

from django.test import TestCase
from rest_framework import status

from app.tests.test_func_tool import TestFuncTool

from app.exceptions import message_constants


class UserEntityTest(TestCase):

    def setUp(self):
        self.test_tool = TestFuncTool()
        self.auth_header_prefix = "Bearer "

        filejson = open('./app/tests/data/user_data.json', encoding='utf-8')
        self.user_data = json.loads(filejson.read())

    def equal_user(self, body, user):
        self.assertEqual(body['id'], user.id)
        self.assertEqual(body['role_id'], user.role_id)
        self.assertEqual(body['username'], user.username)
        self.assertEqual(body['name'], user.name)
        self.assertEqual(body['surname'], user.surname)
        self.assertEqual(body['phone'], user.phone)
        self.assertEqual(body['email'], user.email)

    def equal_role(self, body, role):
        self.assertEqual(body['id'], role.id)
        self.assertEqual(body['name'], role.name)


    def test_user_should_get_access_with_token(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/user/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.equal_user(body['user'], user_orm)

    def test_should_return_error_if_token_not_valid(self):
        not_valid_token = 'qwerthjhgfdsasdfghjhgfddghjhdfgb'

        route = '/api/user/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + not_valid_token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['user']['detail'], message_constants.INVALID_AUTH_TOKEN)

    def test_should_return_error_if_header_prefix_is_not_bearer(self):
        not_valid_header_prefix = "Something"

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/user/'
        header = {"HTTP_AUTHORIZATION": not_valid_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['user']['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_error_if_user_is_not_active(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        user_orm.is_active = False
        user_orm.save()

        route = '/api/user/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['user']['detail'], message_constants.NOT_ACTIVE_USER)

    def test_should_return_error_if_user_not_found_by_token(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        user_orm.delete()

        route = '/api/user/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['user']['detail'], message_constants.USER_NOT_FOUND)

    def test_should_return_user_if_email_and_password_is_correct(self):
        user_password = 'example_password'

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)

        user_orm.set_password(user_password)
        user_orm.save()

        route = '/api/users/login/'
        data = json.dumps({
            "email": user_orm.email,
            "password": user_password
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(body['user']['username'], user_orm.username)
        self.assertEqual(body['user']['email'], user_orm.email)
        self.assertEqual(body['user']['token'], user_orm._generate_jwt_token())

    def test_should_return_error_if_email_field_not_sent(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)

        route = '/api/users/login/'
        data = json.dumps({
            "password": user_orm.password
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(body['user']['errors']['email'][0], "This field is required.")

    def test_should_return_error_if_password_field_not_sent(self):

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)

        route = '/api/users/login/'
        data = json.dumps({
            "email": user_orm.email,
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(body['user']['errors']['password'][0], "This field is required.")

    def test_should_return_error_if_user_not_found_with_email_and_password(self):
        doesnt_exist_user_email = "example@test.com"
        user_password = "qwerty"

        route = '/api/users/login/'
        data = json.dumps({
            "email": doesnt_exist_user_email,
            "password": user_password
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(body['user']['errors']['error'][0], message_constants.USER_NOT_FOUND_WITH_EMAIL_AND_PASSWORD)

    def test_login_should_return_error_if_user_is_not_active(self):
        user_password = "qwerty"

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)

        user_orm.set_password(user_password)
        user_orm.save()

        user_orm.is_active = False
        user_orm.save()

        route = '/api/users/login/'
        data = json.dumps({
            "email": user_orm.email,
            "password": user_password
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(body['user']['errors']['error'][0], message_constants.NOT_ACTIVE_USER)

    def test_should_authenticate_and_return_user_if_entered_fields_are_valid(self):
        role = self.test_tool.create_role_orm()

        user_personal_info = self.user_data['user']
        user_personal_info['role_id'] = role.id

        route = '/api/users/signup/'
        data = json.dumps(user_personal_info)

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['user']['username'], user_personal_info['username'])
        self.assertEqual(body['user']['email'], user_personal_info['email'])
        self.assertEqual(body['user']['phone'], user_personal_info['phone'])
        self.assertEqual(body['user']['role_id'], user_personal_info['role_id'])

    def test_should_return_error_if_user_didnt_send_required_fields(self):
        role = self.test_tool.create_role_orm()

        user_personal_info = self.user_data['user']
        user_personal_info['role_id'] = role.id

        route = '/api/users/signup/'
        required_fields = ['username', 'email', 'phone', 'name', 'surname']

        for required_field in required_fields:
            del user_personal_info[required_field]

            data = json.dumps(user_personal_info)

            response = self.client.post(route, data, content_type="application/json")
            body = json.loads(response.content.decode())

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(body['user']['errors'][required_field][0], 'This field is required.')

    def test_should_return_error_if_user_send_required_fields_as_null(self):
        role = self.test_tool.create_role_orm()

        user_personal_info = self.user_data['user']
        user_personal_info['role_id'] = role.id

        route = '/api/users/signup/'
        required_fields = ['username', 'email', 'phone', 'name', 'surname']

        for required_field in required_fields:
            user_personal_info[required_field] = None

            data = json.dumps(user_personal_info)

            response = self.client.post(route, data, content_type="application/json")
            body = json.loads(response.content.decode())

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(body['user']['errors'][required_field][0], 'This field may not be null.')

    def test_should_return_error_if_user_send_required_fields_as_blank(self):
        role = self.test_tool.create_role_orm()

        user_personal_info = self.user_data['user']
        user_personal_info['role_id'] = role.id

        route = '/api/users/signup/'
        required_fields = ['username', 'email', 'phone', 'name', 'surname']

        for required_field in required_fields:
            user_personal_info[required_field] = ''

            data = json.dumps(user_personal_info)

            response = self.client.post(route, data, content_type="application/json")
            body = json.loads(response.content.decode())

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(body['user']['errors'][required_field][0], 'This field may not be blank.')

    def test_should_return_error_if_email_not_valid(self):
        not_valid_email = 'not_valid_email'
        role = self.test_tool.create_role_orm()

        user_personal_info = self.user_data['user']
        user_personal_info['role_id'] = role.id
        user_personal_info['email'] = not_valid_email

        route = '/api/users/signup/'
        data = json.dumps(user_personal_info)

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(body['user']['errors']['email'][0], 'Enter a valid email address.')

    def test_should_update_user_with_valid_data(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        new_role_orm = self.test_tool.create_role_orm(name='example role #2')
        new_name = 'NewName'
        new_surname = 'NewSurName'
        new_email = 'new_email@example.com'
        new_phone = 'NewPhone'
        new_username = 'NewUserName'
        new_password = 'NewPassword'

        route = '/api/user/'
        data = json.dumps({
            "role_id": new_role_orm.id,
            "name": new_name,
            "surname": new_surname,
            "email": new_email,
            "phone": new_phone,
            "username": new_username,
            "password": new_password
        })
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.put(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(body['user']['name'], new_name)
        self.assertEqual(body['user']['surname'], new_surname)
        self.assertEqual(body['user']['username'], new_username)
        self.assertEqual(body['user']['email'], new_email)
        self.assertEqual(body['user']['phone'], new_phone)
        self.assertEqual(body['user']['role_id'], new_role_orm.id)

    def test_should_return_error_if_user_didnt_send_auth_token(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)

        new_role_orm = self.test_tool.create_role_orm(name='example role #2')
        new_name = 'NewName'
        new_surname = 'NewSurName'
        new_email = 'new_email@example.com'
        new_phone = 'NewPhone'
        new_username = 'NewUserName'
        new_password = 'NewPassword'

        route = '/api/user/'
        data = json.dumps({
            "role_id": new_role_orm.id,
            "name": new_name,
            "surname": new_surname,
            "email": new_email,
            "phone": new_phone,
            "username": new_username,
            "password": new_password
        })
        header = {"HTTP_AUTHORIZATION": ''}

        response = self.client.put(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['user']['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_all_user(self):
        user_phone = '+99677911111'
        user_email = 'example@example.com'
        username = 'username #'

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        other_users_count = 5
        all_users = [user_orm]
        for i in range(other_users_count):
            user_orm = self.test_tool.create_user_orm(
                role_id=role_orm.id,
                phone=user_phone + str(i),
                email=str(i) + user_email,
                username=username + str(i)
            )
            all_users.append(user_orm)

        route = '/api/users/all/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for index in range(other_users_count):
            self.equal_user(body[index], all_users[index])

    def test_get_all_users_should_return_error_if_user_doesnt_send_auth_token(self):
        user_phone = '+99677911111'
        user_email = 'example@example.com'
        username = 'username #'

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)

        other_users_count = 5
        all_users = [user_orm]
        for i in range(other_users_count):
            user_orm = self.test_tool.create_user_orm(
                role_id=role_orm.id,
                phone=user_phone + str(i),
                email=str(i) + user_email,
                username=username + str(i)
            )
            all_users.append(user_orm)

        route = '/api/users/all/'

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_delete_user_by_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/user/'
        data = json.dumps({
            "user_id": user_orm.id
        })
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.delete(route, data, content_type="application/json", **header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_all_roles(self):
        role_name = 'role #'
        role_count = 5

        all_roles = []
        for i in range(role_count):
            role_orm = self.test_tool.create_role_orm(
                name=role_name + str(i)
            )
            all_roles.append(role_orm)

        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/roles/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(role_count):
            self.equal_role(body[i], all_roles[i])

    def test_get_all_roles_should_return_error_if_user_didnt_send_auth_token(self):
        role_name = 'role #'
        role_count = 5

        all_roles = []
        for i in range(role_count):
            role_orm = self.test_tool.create_role_orm(
                name=role_name + str(i)
            )
            all_roles.append(role_orm)

        route = '/api/roles/'

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_create_new_role_with_valid_only_field_name(self):
        new_role_name = 'role #2'
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/roles/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            'name': new_role_name
        })

        response = self.client.post(route,  data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['name'], new_role_name)

    def test_create_role_should_return_error_if_user_didnt_send_auth_token(self):
        new_role_name = 'role #2'

        route = '/api/roles/'
        data = json.dumps({
            'name': new_role_name
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_delete_role_by_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()
        other_empty_role_orm = self.test_tool.create_role_orm()

        route = '/api/roles/'
        data = json.dumps({
            "role_id": other_empty_role_orm.id
        })
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.delete(route, data, content_type="application/json", **header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_error_if_role_not_found_with_id(self):
        does_not_exist_role_id = 12345678

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/roles/'
        data = json.dumps({
            "role_id": does_not_exist_role_id
        })
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.delete(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], message_constants.ENTITY_NOT_FOUND)

    def test_should_return_error_if_users_exist_with_this_role(self):

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/roles/'
        data = json.dumps({
            "role_id": role_orm.id
        })
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.delete(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(body['errors'][0], message_constants.USERS_EXIST_WITH_ROLE)

    def test_delete_role_should_return_error_if_user_doesnt_send_auth_token(self):

        role_orm = self.test_tool.create_role_orm()
        other_empty_role_orm = self.test_tool.create_role_orm()

        route = '/api/roles/'
        data = json.dumps({
            "role_id": other_empty_role_orm.id
        })

        response = self.client.delete(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)