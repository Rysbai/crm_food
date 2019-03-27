
from django.db import models

from .meal import Meal
from .user import User


class Status(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Table(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):
    waiter = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    isitopen = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.meals.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='meals', on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.meal.price * self.count
