
from rest_framework import serializers

from app.models.order import Table, Order, OrderItem, Status
from app.models.meal import Meal


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name')


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'name')


class OrderItemSerializer(serializers.ModelSerializer):
    meal_id = serializers.PrimaryKeyRelatedField(
        queryset=Meal.objects.all(),
        source='meal.id',
    )
    name = serializers.CharField(
        source='meal.name',
        read_only=True
    )
    price = serializers.CharField(
        source='meal.price',
        read_only=True
    )
    total = serializers.FloatField(source='get_cost', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('meal_id', 'name', 'price', 'count', 'total')


class OrderSerializer(serializers.ModelSerializer):
    waiter_id = serializers.IntegerField(
        source='waiter.id',
        read_only=True
    )
    isitopen = serializers.BooleanField(
        read_only=True,
        default=True
    )
    table_id = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(),
        source='table.id',
    )
    table_name = serializers.CharField(
        source='table.name',
        read_only=True
    )
    meals = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'waiter_id', 'date', 'isitopen', 'table_id', 'table_name', 'meals')

    def create(self, validated_data):
        order = Order.objects.create(
            waiter=validated_data['waiter'],
            table=validated_data['table']['id'],
        )
        if 'meals' in validated_data:
            for meal in validated_data['meals']:
                OrderItem.objects.create(
                    order=order,
                    meal=meal['meal']['id'],
                    count=meal['count']
                ).save()
        order.save()

        return order


class MealsInOrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(
        source='id',
    )
    meals = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('order_id', 'meals')

    def create(self, validated_data):
        order = Order.objects.get(id=validated_data['id'])
        for meal in validated_data['meals']:
            OrderItem.objects.create(
                order=order,
                meal=meal['meal']['id'],
                count=meal['count']
            ).save()
        order.save()

        return order
