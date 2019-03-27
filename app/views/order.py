import datetime
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError

from app.models.order import Status, Table, Order
from app.models.meal import Meal

from app.serializers.order import StatusSerializer, TableSerializer, \
                                    OrderSerializer, MealsInOrderSerializer


class StatusView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get(self, request, *args, **kwargs):
        statuses = self.queryset.all()
        serializer = self.serializer_class(statuses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        status_id = request.data.get('id', None)

        if status_id is None:
            raise ParseError("status_id field is required!")

        try:
            status_obj = self.queryset.get(id=status_id)
        except Status.DoesNotExist:
            raise Http404
        else:
            status_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TableView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def get(self, request, *args, **kwargs):
        tables = self.queryset.all()
        serializer = self.serializer_class(tables, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        table_id = request.data.get('id', None)

        if table_id is None:
            raise ParseError("table_id field is required!")

        try:
            table = self.queryset.get(id=table_id)
        except Status.DoesNotExist:
            raise Http404
        else:
            table.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, pk=None, *args, **kwargs):
        if request.query_params.get('days'):
            days = int(request.query_params.get('days'))

            orders = self.queryset.filter(
                date__gt=datetime.datetime.now() - datetime.timedelta(days=days)
            ).order_by('-date')
            serializer = self.serializer_class(orders, many=True)

            return Response(serializer.data)

        if pk:
            try:
                order = self.queryset.get(id=pk)
            except Order.DoesNotExist:
                raise Http404
            else:
                serializer = self.serializer_class(order)
                return Response(serializer.data, status=status.HTTP_200_OK)

        orders = self.queryset.all()
        serializer = self.serializer_class(orders, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(waiter=self.request.user)

    def delete(self, request, *args, **kwargs):
        order_id = request.data.get('id', None)

        if order_id is None:
            raise ParseError("order_id field is required!")

        try:
            order = self.queryset.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404
        else:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)



class GetActiveOrderListView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request):
        orders = self.queryset.filter(isitopen=True)
        serializer = self.serializer_class(orders, many=True)

        return Response(serializer.data)


class MealsInOrderView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = MealsInOrderSerializer

    def get(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        try:
            order = self.queryset.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(order)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        order_id = request.data.get('order_id', None)
        meal_id = request.data.get('meal_id', None)

        if order_id is None:
            raise ParseError("order_id field is required!")

        if meal_id is None:
            raise ParseError("meal_id field is required!")

        try:
            order = self.queryset.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404

        try:
            meal = order.meals.get(id=meal_id)
        except Meal.DoesNotExist:
            raise Http404

        meal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)





