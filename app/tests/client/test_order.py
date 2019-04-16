import json

from django.test import TestCase
from rest_framework import status

from app.exceptions import message_constants
from app.tests.test_func_tool import TestFuncTool


class OrderEntityTest(TestCase):

    def setUp(self):
        self.test_tool = TestFuncTool()
        self.auth_header_prefix = "Bearer "

        filejson = open('./app/tests/data/order_data.json', encoding='utf-8')
        self.meal_data = json.loads(filejson.read())