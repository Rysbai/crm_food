import json

from django.test import TestCase
from rest_framework import status

from app.exceptions import message_constants
from app.tests.test_func_tool import TestFuncTool


class MealEntityTest(TestCase):

    def setUp(self):
        self.test_tool = TestFuncTool()
        self.auth_header_prefix = "Bearer "

        filejson = open('./app/tests/data/meal_data.json', encoding='utf-8')
        self.meal_data = json.loads(filejson.read())

    def equal_department(self, body, department):
        self.assertEqual(body['id'], department.id)
        self.assertEqual(body['name'], department.name)

    def equal_meals_category(self, body, meals_category):
        self.assertEqual(body['id'], meals_category.id)
        self.assertEqual(body['department_id'], meals_category.department_id)
        self.assertEqual(body['name'], meals_category.name)

    def equal_meal(self, body, meal):
        self.assertEqual(body['id'], meal.id)
        self.assertEqual(body['category_id'], meal.category_id)
        self.assertEqual(body['name'], meal.name)
        self.assertEqual(body['price'], meal.price)
        self.assertEqual(body['description'], meal.description)


    def test_should_return_all_departments(self):

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        department_name = 'department #'
        departments_count = 4
        all_departments = []

        for i in range(departments_count):
            department_orm = self.test_tool.create_department_orm(
                name=department_name + str(i)
            )
            all_departments.append(department_orm)

        route = '/api/departments/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(departments_count):
            self.equal_department(body[i], all_departments[i])

    def test_get_all_departments_should_return_error_if_user_didnt_send_auth_token(self):

        department_name = 'department #'
        departments_count = 4
        all_departments = []

        for i in range(departments_count):
            department_orm = self.test_tool.create_department_orm(
                name=department_name + str(i)
            )
            all_departments.append(department_orm)

        route = '/api/departments/'

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_create_department_with_valid_data(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/departments/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps(
            self.meal_data['department']
        )
        response = self.client.post(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['name'], self.meal_data['department']['name'])

    def test_create_department_should_return_error_if_user_didnt_send_auth_token(self):
        route = '/api/departments/'
        data = json.dumps(
            self.meal_data['department']
        )
        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_delete_department_by_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        department_orm = self.test_tool.create_department_orm()

        route = '/api/departments/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": department_orm.id
        })
        response = self.client.delete(route, data, content_type="application/json", **header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_error_if_department_not_found_by_id(self):
        doesnt_exist_department_id = 1234567

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/departments/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": doesnt_exist_department_id
        })

        response = self.client.delete(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], message_constants.ENTITY_NOT_FOUND)

    def test_delete_department_should_return_error_if_user_didnt_send_auth_token(self):
        department_orm = self.test_tool.create_department_orm()

        route = '/api/departments/'
        data = json.dumps({
            "id": department_orm.id
        })
        response = self.client.delete(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_all_meal_categories(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        department_orm = self.test_tool.create_department_orm()
        meal_categories_count = 4
        meals_category_name = 'meals category #'
        all_meal_categories = []

        for i in range(meal_categories_count):
            meals_category_orm = self.test_tool.create_meals_category_orm(
                name=meals_category_name + str(i),
                department_id=department_orm.id
            )
            all_meal_categories.append(meals_category_orm)

        route = '/api/meal_categories/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(meal_categories_count):
            self.equal_meals_category(body[i], all_meal_categories[i])

    def test_get_all_meal_categories_should_return_error_if_user_didnt_send_auth_token(self):
        route = '/api/meal_categories/'

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_create_meals_category_with_valid_data(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        department_orm = self.test_tool.create_department_orm()
        route = '/api/meal_categories/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            'department_id': department_orm.id,
            'name': self.meal_data['meals_category']['name']
        })
        response = self.client.post(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['name'], self.meal_data['meals_category']['name'])

    def test_create_meal_category_should_return_error_if_user_didnt_send_auth_token(self):
        department_orm = self.test_tool.create_department_orm()

        route = '/api/meal_categories/'
        data = json.dumps({
            'department_id': department_orm.id,
            'name': self.meal_data['meals_category']['name']
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_delete_meals_category_by_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )

        route = '/api/meal_categories/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            'id': meals_category_orm.id,
        })
        response = self.client.delete(route, data, content_type="application/json", **header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_error_if_meals_category_not_found_with_sent_id(self):
        doesnt_exist_meals_category_id = 1234567

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/meal_categories/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": doesnt_exist_meals_category_id
        })

        response = self.client.delete(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], message_constants.ENTITY_NOT_FOUND)

    def test_delete_meals_category_should_return_error_if_user_didnt_send_auth_token(self):
        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )

        route = '/api/meal_categories/'
        data = json.dumps({
            'id': meals_category_orm.id,
        })
        response = self.client.delete(route, data, content_type="application/json",)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_all_meals_category_in_sent_department_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        department_orm = self.test_tool.create_department_orm()
        meal_categories_count = 4
        meals_category_name = 'meals category #'
        all_meal_categories = []

        for i in range(meal_categories_count):
            meals_category_orm = self.test_tool.create_meals_category_orm(
                name=meals_category_name + str(i),
                department_id=department_orm.id
            )
            all_meal_categories.append(meals_category_orm)

        route = '/api/meal_categories/by_department/{}/'.format(department_orm.id)
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(meal_categories_count):
            self.equal_meals_category(body[i], all_meal_categories[i])

    def test_should_return_error_department_not_found_by_id(self):
        doesnt_exist_department_id = 123456
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/meal_categories/by_department/{}/'.format(doesnt_exist_department_id)
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], message_constants.ENTITY_NOT_FOUND)

    def test_should_return_error_if_user_didnt_send_auth_token(self):
        doesnt_exist_department_id = 123456
        route = '/api/meal_categories/by_department/{}/'.format(doesnt_exist_department_id)

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_all_meals(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )

        route = '/api/meals/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "category_id": meals_category_orm.id,
            "name": self.meal_data['meal']['name'],
            "price": self.meal_data['meal']['price'],
            "description": self.meal_data['meal']['description']
        })
        response = self.client.post(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['category_id'], meals_category_orm.id)
        self.assertEqual(body['name'], self.meal_data['meal']['name'])
        self.assertEqual(body['price'], self.meal_data['meal']['price'])
        self.assertEqual(body['description'], self.meal_data['meal']['description'])

    def test_create_meal_should_return_error_if_user_didnt_send_auth_token(self):
        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )

        route = '/api/meals/'
        data = json.dumps({
            "category_id": meals_category_orm.id,
            "name": self.meal_data['meal']['name'],
            "price": self.meal_data['meal']['price'],
            "description": self.meal_data['meal']['description']
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_delete_meal_by_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        route = '/api/meals/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": meal_orm.id,
        })

        response = self.client.delete(route, data, content_type="application/json", **header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_error_meal_not_found_by_id(self):
        doesnt_exist_meal_id = 123456
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/meals/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": doesnt_exist_meal_id,
        })

        response = self.client.delete(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], message_constants.ENTITY_NOT_FOUND)

    def test_delete_meal_should_return_error_if_user_didnt_send_auth_token(self):
        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        route = '/api/meals/'
        data = json.dumps({
            "id": meal_orm.id,
        })

        response = self.client.delete(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)