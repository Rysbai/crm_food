
from rest_framework import serializers

from app.models.meal import Department, MealsCategory, Meal


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class MealsCategorySerializer(serializers.ModelSerializer):
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department.id'
    )
    class Meta:
        model = MealsCategory
        fields = ('id', 'department_id', 'name')

    def create(self, validated_data):
        meals_category = MealsCategory.objects.create(
            department=validated_data['department']['id'],
            name=validated_data['name']
        )
        return meals_category


class MealSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=MealsCategory.objects.all(),
        source='category.id'
    )
    class Meta:
        model = Meal
        fields = ('id', 'category_id', 'name', 'price', 'description')

    def create(self, validated_data):
        meal = Meal.objects.create(
            category=validated_data['category']['id'],
            name=validated_data['name'],
            price=validated_data['price'],
            description=validated_data['description']
        )
        return meal
