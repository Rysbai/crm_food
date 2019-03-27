
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MealsCategory(models.Model):
    department = models.ForeignKey(Department, related_name='department', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Meal(models.Model):
    category = models.ForeignKey(MealsCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
