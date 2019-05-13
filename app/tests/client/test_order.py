import json
import datetime
from django.utils import timezone
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

        self.test_objects_counts = 4

    def equal_status(self, body, status):
        self.assertEqual(body['id'], status.id)
        self.assertEqual(body['name'], status.name)

    def equal_table(self, body, table):
        self.assertEqual(body['id'], table.id)
        self.assertEqual(body['name'], table.name)

    def equal_order(self, body, order):
        self.assertEqual(body['id'], order.id)
        self.assertEqual(body['waiter_id'], order.waiter_id)
        self.assertEqual(body['table_id'], order.table_id)
        self.assertEqual(body['table_name'], order.table.name)
        self.assertEqual(body['isitopen'], order.isitopen)

    def equal_order_item(self, body, order_item):
        self.assertEqual(body['meal_id'], order_item.meal_id)
        self.assertEqual(body['count'], order_item.count)
        self.assertEqual(body['total'], order_item.get_cost())

    def test_should_return_all_statuses(self):
        status_name = 'status #'

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        all_statuses = []
        for i in range(self.test_objects_counts):
            status_orm = self.test_tool.create_status_orm(
                name=status_name + str(i)
            )
            all_statuses.append(status_orm)

        route = '/api/statuses/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(self.test_objects_counts):
            self.equal_status(body[i], all_statuses[i])

    def test_get_all_statuses_should_return_error_if_user_didnt_send_auth_token(self):
        status_name = 'status #'

        all_statuses = []
        for i in range(self.test_objects_counts):
            status_orm = self.test_tool.create_status_orm(
                name=status_name + str(i)
            )
            all_statuses.append(status_orm)

        route = '/api/statuses/'

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_create_status_with_valid_fields(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/statuses/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps(
            self.meal_data['status']
        )
        response = self.client.post(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['name'], self.meal_data['status']['name'])

    def test_create_status_should_return_error_if_user_didnt_send_auth_token(self):
        route = '/api/statuses/'
        data = json.dumps(
            self.meal_data['status']
        )
        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_delete_status_by_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        status_orm = self.test_tool.create_status_orm()

        route = '/api/statuses/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": status_orm.id
        })
        response = self.client.delete(route, data, content_type="application/json", **header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_error_if_status_not_found_by_id(self):
        doesnt_exist_status_id = 1234567

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/statuses/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": doesnt_exist_status_id
        })

        response = self.client.delete(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], message_constants.ENTITY_NOT_FOUND)

    def test_delete_status_should_return_error_if_user_didnt_send_auth_token(self):
        status_orm = self.test_tool.create_status_orm()

        route = '/api/statuses/'
        data = json.dumps({
            "id": status_orm.id
        })
        response = self.client.delete(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_all_tables(self):
        table_name = 'status #'

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        all_tables = []
        for i in range(self.test_objects_counts):
            status_orm = self.test_tool.create_table_orm(
                name=table_name + str(i)
            )
            all_tables.append(status_orm)

        route = '/api/tables/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(self.test_objects_counts):
            self.equal_table(body[i], all_tables[i])

    def test_get_all_tables_should_return_if_user_didnt_send_auth_token(self):
        table_name = 'status #'

        all_tables = []
        for i in range(self.test_objects_counts):
            status_orm = self.test_tool.create_table_orm(
                name=table_name + str(i)
            )
            all_tables.append(status_orm)

        route = '/api/tables/'

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_create_table_with_valid_fields(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/tables/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps(
            self.meal_data['table']
        )
        response = self.client.post(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['name'], self.meal_data['table']['name'])

    def test_create_table_should_return_error_if_user_didnt_send_auth_token(self):
        route = '/api/statuses/'
        data = json.dumps(
            self.meal_data['table']
        )
        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_delete_table_by_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        table_orm = self.test_tool.create_table_orm()

        route = '/api/tables/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": table_orm.id
        })
        response = self.client.delete(route, data, content_type="application/json", **header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_error_if_table_not_found_by_id(self):
        doesnt_exist_table_id = 1234567

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/tables/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "id": doesnt_exist_table_id
        })

        response = self.client.delete(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], message_constants.ENTITY_NOT_FOUND)

    def test_delete_table_should_return_error_if_user_didnt_send_auth_token(self):
        table_orm = self.test_tool.create_status_orm()

        route = '/api/tables/'
        data = json.dumps({
            "id": table_orm.id
        })
        response = self.client.delete(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_all_orders(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        all_orders = []
        for i in range(self.test_objects_counts):
            order_orm = self.test_tool.create_order_orm(
                table_id=table_orm.id,
                waiter_id=user_orm.id
            )
            _order_item_orm = self.test_tool.create_order_item_orm(
                meal_id=meal_orm.id,
                order_id=order_orm.id,
                count=3
            )
            all_orders.append(order_orm)

        route = '/api/orders/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i in range(self.test_objects_counts):
            self.equal_order(body[i], all_orders[i])
            self.equal_order_item(body[i]['meals'][0], all_orders[i].meals.all()[0])

    def test_get_all_orders_should_return_error_if_user_didnt_send_auth_token(self):

        route = '/api/orders/'

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_orders_in_given_last_days(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        days = 7
        order_counts_in_given_last_days = self.test_objects_counts - 2
        orders_in_given_last_days = []

        for i in range(self.test_objects_counts):
            if i < order_counts_in_given_last_days:
                order_orm = self.test_tool.create_order_orm(
                    table_id=table_orm.id,
                    waiter_id=user_orm.id
                )
                _order_item_orm = self.test_tool.create_order_item_orm(
                    meal_id=meal_orm.id,
                    order_id=order_orm.id,
                    count=3
                )
                order_orm.date = timezone.now() - datetime.timedelta(days=days-1, hours=23, minutes=59)
                order_orm.save()
                orders_in_given_last_days.insert(0, order_orm)

            else:
                order_orm = self.test_tool.create_order_orm(
                    table_id=table_orm.id,
                    waiter_id=user_orm.id
                )
                order_orm.date = timezone.now() - datetime.timedelta(days=days, seconds=1)
                order_orm.save()

        route = '/api/orders?days={}'.format(days)
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(body), order_counts_in_given_last_days)

        for i in range(order_counts_in_given_last_days):
            self.equal_order(body[i], orders_in_given_last_days[i])
            self.equal_order_item(body[i]['meals'][0], orders_in_given_last_days[i].meals.all()[0])

    def test_should_create_order_with_valid_data(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)
        meals_count = 5

        route = '/api/orders/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}
        data = json.dumps({
            "table_id": table_orm.id,
            "meals": [
                {
                    "meal_id": meal_orm.id,
                    "count": meals_count
                }
            ]
        })

        response = self.client.post(route, data, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(body['waiter_id'], user_orm.id)
        self.assertEqual(body['table_id'], table_orm.id)
        self.assertEqual(body['isitopen'], True)

        self.assertEqual(body['meals'][0]['meal_id'], meal_orm.id)
        self.assertEqual(body['meals'][0]['count'], meals_count)
        self.assertEqual(body['meals'][0]['total'], meal_orm.price * meals_count)

    def test_create_order_should_return_error_if_user_didnt_send_auth_token(self):
        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)
        meals_count = 5

        route = '/api/orders/'
        data = json.dumps({
            "table_id": table_orm.id,
            "meals": [
                {
                    "meal_id": meal_orm.id,
                    "count": meals_count
                }
            ]
        })

        response = self.client.post(route, data, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_order_by_id(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        order_orm = self.test_tool.create_order_orm(
            table_id=table_orm.id,
            waiter_id=user_orm.id
        )
        order_item_orm = self.test_tool.create_order_item_orm(
            meal_id=meal_orm.id,
            order_id=order_orm.id,
            count=3
        )

        route = '/api/orders/{}/'.format(order_orm.id)
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.equal_order(body, order_orm)
        self.equal_order_item(body['meals'][0], order_item_orm)

    def test_should_return_error_if_order_not_found_by_id(self):
        doesnt_exist_order_id = 123456

        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        route = '/api/orders/{}/'.format(doesnt_exist_order_id)
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], message_constants.ENTITY_NOT_FOUND)

    def test_get_order_by_id_should_return_error_if_user_didnt_send_auth_token(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)

        table_orm = self.test_tool.create_table_orm()
        order_orm = self.test_tool.create_order_orm(
            table_id=table_orm.id,
            waiter_id=user_orm.id
        )

        route = '/api/orders/{}/'.format(order_orm.id)

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_active_orders(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        active_orders_count = self.test_objects_counts - 2
        active_orders = []

        for i in range(self.test_objects_counts):
            if i < active_orders_count:
                order_orm = self.test_tool.create_order_orm(
                    table_id=table_orm.id,
                    waiter_id=user_orm.id
                )
                _order_item_orm = self.test_tool.create_order_item_orm(
                    meal_id=meal_orm.id,
                    order_id=order_orm.id,
                    count=3
                )
                active_orders.append(order_orm)

            else:
                order_orm = self.test_tool.create_order_orm(
                    table_id=table_orm.id,
                    waiter_id=user_orm.id
                )
                order_orm.isitopen = False
                order_orm.save()

        route = '/api/orders/active_orders/'
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(body), active_orders_count)

        for i in range(active_orders_count):
            self.equal_order(body[i], active_orders[i])
            self.equal_order_item(body[i]['meals'][0], active_orders[i].meals.all()[0])

    def test_get_active_orders_should_return_error_if_user_didnt_send_auth_token(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)

        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        active_orders_count = self.test_objects_counts - 2
        active_orders = []

        for i in range(self.test_objects_counts):
            if i < active_orders_count:
                order_orm = self.test_tool.create_order_orm(
                    table_id=table_orm.id,
                    waiter_id=user_orm.id
                )
                _order_item_orm = self.test_tool.create_order_item_orm(
                    meal_id=meal_orm.id,
                    order_id=order_orm.id,
                    count=3
                )
                active_orders.append(order_orm)

            else:
                order_orm = self.test_tool.create_order_orm(
                    table_id=table_orm.id,
                    waiter_id=user_orm.id
                )
                order_orm.isitopen = False
                order_orm.save()

        route = '/api/orders/active_orders/'

        response = self.client.get(route, content_type="application/json")
        body = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], message_constants.AUTH_NOT_PROVIDED)

    def test_should_return_meals_of_given_order(self):
        role_orm = self.test_tool.create_role_orm()
        user_orm = self.test_tool.create_user_orm(role_id=role_orm.id)
        token = user_orm._generate_jwt_token()

        table_orm = self.test_tool.create_table_orm()

        department_orm = self.test_tool.create_department_orm()
        meals_category_orm = self.test_tool.create_meals_category_orm(
            department_id=department_orm.id
        )
        order_orm = self.test_tool.create_order_orm(
            table_id=table_orm.id,
            waiter_id=user_orm.id
        )
        meal_orm = self.test_tool.create_meal_orm(category_id=meals_category_orm.id)

        meals_in_order_count = self.test_objects_counts - 2
        order_items = []

        for i in range(self.test_objects_counts):
            if i < meals_in_order_count:

                order_item_orm = self.test_tool.create_order_item_orm(
                    meal_id=meal_orm.id,
                    order_id=order_orm.id,
                    count=3
                )
                order_items.append(order_item_orm)

            else:
                other_order_orm = self.test_tool.create_order_orm(
                    table_id=table_orm.id,
                    waiter_id=user_orm.id
                )
                _order_item_orm = self.test_tool.create_order_item_orm(
                    meal_id=meal_orm.id,
                    order_id=other_order_orm.id,
                    count=3
                )

        route = '/api/order/meals?order_id={}/'.format(order_orm.id)
        header = {"HTTP_AUTHORIZATION": self.auth_header_prefix + token}

        response = self.client.get(route, content_type="application/json", **header)
        body = json.loads(response.content.decode())

        for i in range(meals_in_order_count):
            self.equal_order(body['order_id'], order_orm.id)
            self.equal_order_item(body['meals'], order_items[i])
