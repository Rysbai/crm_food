
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError

from app.models.check import ServicePercentage, Check
from app.models.order import Order

from app.serializers.check import ServicePercentageSerializer, CheckSerializer


class ServicePercentageView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = ServicePercentage.objects.all()
    serializer_class = ServicePercentageSerializer

    def get(self, request, *args, **kwargs):
        try:
            percentage = self.queryset.all()[0]
        except IndexError:
            return Response([], status=status.HTTP_200_OK)

        serializer = self.serializer_class(percentage)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        percentage_id = request.data.get('id', None)

        if percentage_id is None:
            raise ParseError("department_id field is required")

        try:
            percentage = self.queryset.get(id=percentage_id)
        except ServicePercentage.DoesNotExist:
            raise Http404
        else:
            percentage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CheckView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def get(self, request, *args, **kwargs):
        checks = self.queryset.all()

        serializer = self.serializer_class(checks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self._close_order(serializer.data['order_id'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        check_id = request.data.get('id', None)

        if check_id is None:
            raise ParseError("department_id field is required")

        try:
            check = self.queryset.get(id=check_id)
        except Check.DoesNotExist:
            raise Http404
        else:
            check.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


    def _close_order(self, order_id):
        order = Order.objects.get(id=order_id)
        order.isitopen = False
        order.save()
