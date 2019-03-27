
from rest_framework import serializers

from app.models.check import ServicePercentage, Check
from app.models.order import Order

from .order import OrderItemSerializer


class ServicePercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePercentage
        fields = ('id', 'percentage')


class MealsInCheckSerializer(serializers.ModelSerializer):
    meals = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('meals', )


class CheckSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        source='order.id'
    )
    servicefee = serializers.FloatField(
        source='percentage.percentage',
        read_only=True
    )
    order = MealsInCheckSerializer(read_only=True)
    total_sum = serializers.FloatField(source='get_total_sum', read_only=True)

    class Meta:
        model = Check
        fields = ['id', 'order_id', 'date', 'servicefee', 'total_sum', 'order']

    def create(self, validated_data):
        percentages = ServicePercentage.objects.all()
        check = Check.objects.create(
            order=validated_data['order']['id'],
            percentage=percentages[0]
        )
        check.save()

        return check
