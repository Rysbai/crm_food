import json
import datetime
from django.utils import timezone
from django.test import TestCase
from rest_framework import status

from app.exceptions import message_constants
from app.tests.test_func_tool import TestFuncTool

from app.models.check import ServicePercentage, Check


class CheckEntityTest(TestCase):

    def setUp(self):
        self.test_tool = TestFuncTool()
        self.auth_header_prefix = "Bearer "

        filejson = open('./app/tests/data/check_data.json', encoding='utf-8')
        self.check_data = json.loads(filejson.read())

        self.test_objects_counts = 4

    def equal_percentage(self, body, percentage):
        self.assertEqual(body['id'], percentage.id)
        self.assertEqual(body['percentage'], percentage.percentage)

    def equal_check(self, body, check):
        self.assertEqual(body['id'], check.id)
        self.assertEqual(body['order_id'], check.order_id)
        self.assertEqual(body['servicefee'], check.percentage.percentage)
        self.assertEqual(body['total_sum'], check.get_total_sum())

    def equal_order_item(self, body, order_item):
        self.assertEqual(body['meal_id'], order_item.meal_id)
        self.assertEqual(body['name'], order_item.meal.name)
        self.assertEqual(body['price'], str(order_item.meal.price))
        self.assertEqual(body['count'], order_item.count)
        self.assertEqual(body['total'], order_item.get_cost())


    def test_should_return_all_service_percentages(self):
        percentage_sum = 30

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        all_percentages = []
        for i in range(self.test_objects_counts):
            percentage_orm = self.test_tool.create_percentage_orm(
                percentage=percentage_sum + i
            )
            all_percentages.append(percentage_orm)

        route = '/api/service_percentage/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(self.test_objects_counts):
            self.equal_percentage(body[i], all_percentages[i])

    def test_get_service_percentages_should_return_error_if_user_didnt_send_auth_token(self):
        percentage_sum = 30

        all_percentages = []
        for i in range(self.test_objects_counts):
            percentage_orm = self.test_tool.create_percentage_orm(
                percentage=percentage_sum + i
            )
            all_percentages.append(percentage_orm)

        route = '/api/service_percentage/'

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_create_service_percentage(self):

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/service_percentage/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps(self.check_data['percentage'])

        response = self.client.post(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['percentage'], self.check_data['percentage']['percentage'])

    def test_create_percentage_should_return_error_if_user_didnt_send_auth_token(self):

        route = '/api/service_percentage/'
        data = json.dumps(self.check_data['percentage'])

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_delete_percentage_by_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        percentage_orm = self.test_tool.create_percentage_orm()

        route = '/api/service_percentage/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": percentage_orm.id
        })

        response = self.client.delete(route, data, content_type="application/json", **header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ServicePercentage.DoesNotExist):
            ServicePercentage.objects.get(id=percentage_orm.id)

    def test_should_return_error_if_percentage_not_found_by_id(self):
        percentage_id = 123456

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/service_percentage/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": percentage_id
        })

        response = self.client.delete(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], message_constants.ENTITY_NOT_FOUND)

    def test_delete_percentage_should_return_error_user_didnt_send_auth_token(self):

        percentage_orm = self.test_tool.create_percentage_orm()

        route = '/api/service_percentage/'
        data = json.dumps({
            "id": percentage_orm.id
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_all_checks(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        table_orm = self.test_tool.create_table_orm()
        percentage_orm = self.test_tool.create_percentage_orm()

        all_checks = []
        for i in range(self.test_objects_counts):
            order_orm = self.test_tool.create_order_orm(
                table_id=table_orm.id,
                waiter_id=user_orm.id
            )
            check_orm = self.test_tool.create_check_orm(
                order_id=order_orm.id,
                percentage_id=percentage_orm.id
            )
            all_checks.append(check_orm)

        route = '/api/checks/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(self.test_objects_counts):
            self.equal_check(body[i], all_checks[i])

    def test_get_all_checks_should_return_403_error_if_user_didnt_send_auth_token(self):

        route = '/api/checks/'
        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_create_check_for_given_order(self):

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        percentage_orm = self.test_tool.create_percentage_orm()

        order_orm = self.test_tool.create_order_orm(
            table_id=table_orm.id,
            waiter_id=user_orm.id
        )
        all_order_items = []
        order_item_orm = self.test_tool.create_order_item_orm(
            meal_id=meal_orm.id,
            order_id=order_orm.id,
            count=3
        )
        all_order_items.append(order_item_orm)

        route = '/api/checks/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "order_id": order_orm.id
        })

        response = self.client.post(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['order_id'], order_orm.id)
        self.assertEqual(body['servicefee'], percentage_orm.percentage)

        for i in range(len(body['order']['meals'])):
            self.equal_order_item(body['order']['meals'][i], all_order_items[i])

    def test_create_check_should_return_403_error_if_user_didnt_send_auth_token(self):

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)

        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        percentage_orm = self.test_tool.create_percentage_orm()

        order_orm = self.test_tool.create_order_orm(
            table_id=table_orm.id,
            waiter_id=user_orm.id
        )
        all_order_items = []
        order_item_orm = self.test_tool.create_order_item_orm(
            meal_id=meal_orm.id,
            order_id=order_orm.id,
            count=3
        )
        all_order_items.append(order_item_orm)

        route = '/api/checks/'
        data = json.dumps({
            "order_id": order_orm.id
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_bad_request_error_if_user_didnt_send_order_id(self):

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/checks/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.post(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(body['errors']['order_id'][0])

    def test_should_return_not_found_error_if_order_was_not_found_by_order_id(self):
        doesnt_exist_order_id = 12345678

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/checks/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        data = json.dumps({
            'order_id': doesnt_exist_order_id
        })

        response = self.client.post(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(body['errors']['order_id'][0])
