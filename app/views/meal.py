
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError

from app.models.meal import Department, MealsCategory, Meal

from app.serializers.meal import DepartmentSerializer, MealsCategorySerializer,\
                                    MealSerializer


class DepartmentView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get(self, request, *args, **kwargs):
        departments = self.queryset.all()
        serializer = self.serializer_class(departments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        department_id = request.data.get('id', None)

        if department_id is None:
            raise ParseError("department_id field is required!")

        try:
            department = self.queryset.get(id=department_id)
        except Department.DoesNotExist:
            raise Http404
        else:
            department.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)


class MealsCategoryView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = MealsCategory.objects.all()
    serializer_class = MealsCategorySerializer

    def get(self, request, department_id=None, *args, **kwargs):
        if department_id:
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                raise Http404
            else:
                meal_categories = self.queryset.filter(department=department).order_by('id')
                serializer = self.serializer_class(meal_categories, many=True)

                return Response(serializer.data)

        meal_categories = self.queryset.all()
        serializer = self.serializer_class(meal_categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        meals_category_id = request.data.get('id', None)

        if meals_category_id is None:
            raise ParseError("meals_category_id field is required!")

        try:
            meals_category = self.queryset.get(id=meals_category_id)
        except MealsCategory.DoesNotExist:
            raise Http404
        else:
            meals_category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class MealsView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def get(self, request, meals_category_id=None, *args, **kwargs):
        if meals_category_id:
            try:
                meals_category = MealsCategory.objects.get(id=meals_category_id)
            except MealsCategory.DoesNotExist:
                raise Http404
            else:
                meals = self.queryset.filter(category=meals_category)
                serializer = MealSerializer(meals, many=True)
                return Response(serializer.data)

        meals = self.queryset.all()
        serializer = self.serializer_class(meals, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        meal_id = request.data.get('id', None)

        if meal_id is None:
            raise ParseError("meals_category_id field is required!")

        try:
            meal = self.queryset.get(id=meal_id)
        except Meal.DoesNotExist:
            raise Http404
        else:
            meal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
