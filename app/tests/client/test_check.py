import json
import datetime
from django.utils import timezone
from django.test import TestCase
from rest_framework import status

from app.exceptions import message_constants
from app.tests.test_func_tool import TestFuncTool


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








