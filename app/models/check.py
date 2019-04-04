
from django.db import models

from .order import Order


class ServicePercentage(models.Model):
    percentage = models.FloatField()

    def __str__(self):
        return self.percentage


class Check(models.Model):
    order = models.ForeignKey(Order, unique=True, on_delete=models.DO_NOTHING)
    percentage = models.ForeignKey(ServicePercentage, on_delete=None)
    date = models.DateTimeField(auto_now_add=True)

    def get_total_sum(self):
        return self.order.get_total_cost() + self.percentage.percentage
