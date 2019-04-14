import json

from app.models.user import Role, User
from app.models.meal import Department, MealsCategory, Meal
from app.models.order import Status, Table, Order, OrderItem
from app.models.check import ServicePercentage, Check


class TestFuncTool:

    def __init__(self):

        filejson = open('./app/tests/data/user_data.json', encoding='utf-8')
        self.user_data = json.loads(filejson.read())

        file_json = open('./app/tests/data/meal_data.json', encoding='utf-8')
        self.meal_data = json.loads(file_json.read())

        file_json = open('./app/tests/data/order_data.json', encoding='utf-8')
        self.order_data = json.loads(file_json.read())

        file_json = open('./app/tests/data/check_data.json', encoding='utf-8')
        self.check_data = json.loads(file_json.read())

    def create_role_orm(self, **kwargs):
        role_data = self.user_data['role'].copy()

        for key, value in kwargs.items():
            role_data[key] = value

        return Role.objects.create(**role_data)

    def create_user_orm(self, **kwargs):
        user_data = self.user_data['user'].copy()

        for key, value in kwargs.items():
            user_data[key] = value

        return User.objects.create(**user_data)

    def create_department_orm(self, **kwargs):
        department_data = self.meal_data['department'].copy()

        for key, value in kwargs.items():
            department_data[key] = value

        return Department.objects.create(**department_data)

    def create_meals_category_orm(self, **kwargs):
        meals_category_data = self.meal_data['meals_category'].copy()

        for key, value in kwargs.items():
            meals_category_data[key] = value

        return MealsCategory.objects.create(**meals_category_data)

    def create_meal_orm(self, **kwargs):
        meal_data = self.meal_data['meal'].copy()

        for key, value in kwargs.items():
            meal_data[key] = value

        return Meal.objects.create(**meal_data)

    def create_table_orm(self, **kwargs):
        table_data = self.order_data['table'].copy()

        for key, value in kwargs.items():
            table_data[key] = value

        return Table.objects.create(**table_data)

    def create_order_orm(self, **kwargs):
        order_data = self.order_data['order'].copy()

        for key, value in kwargs.items():
            order_data[key] = value

        return Order.objects.create(**order_data)

    def create_order_item_orm(self, **kwargs):
        order_item_data = self.order_data['order_item'].copy()

        for key, value in kwargs.items():
            order_item_data[key] = value

        return OrderItem.objects.create(**order_item_data)

    def create_status_orm(self, **kwargs):
        status_data = self.order_data['status'].copy()

        for key, value in kwargs.items():
            status_data[key] = value

        return Status.objects.create(**status_data)

    def create_percentage_orm(self, **kwargs):
        percentage_data = self.check_data['percentage'].copy()

        for key, value in kwargs.items():
            percentage_data[key] = value

        return ServicePercentage.objects.create(**percentage_data)

    def create_check_orm(self, **kwargs):
        check_data = self.check_data['check'].copy()

        for key, value in kwargs.items():
            check_data[key] = value

        return Check.objects.create(**check_data)

