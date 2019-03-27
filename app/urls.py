
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from app.views.login_sign_up import RegistrationAPIView, RoleView, \
                                    LoginView, UserRetrieveUpdateAPIView

from app.views.meal import DepartmentView, MealsCategoryView, MealsView

from app.views.order import StatusView, \
                            TableView, OrderView, \
                            GetActiveOrderListView, \
                            MealsInOrderView


from app.views.check import ServicePercentageView, CheckView


urlpatterns = [
    path('roles/', RoleView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginView.as_view()),

    path('departments/', DepartmentView.as_view()),

    path('meal_categories/', MealsCategoryView.as_view()),
    path('meal_categories/by_department/<int:department_id>/',
        MealsCategoryView.as_view()),

    path('meals/', MealsView.as_view()),
    path('meals/by_category/<int:meals_category_id>/',  MealsView.as_view()),

    path('statuses/', StatusView.as_view()),
    path('service_persentage/', ServicePercentageView.as_view()),
    path('tables/', TableView.as_view()),

    path('orders/', OrderView.as_view()),
    path('orders/active_orders/', GetActiveOrderListView.as_view()),

    path('order/<int:pk>/', OrderView.as_view()),
    path('order/meals/', MealsInOrderView.as_view()),

    path('checks/', CheckView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
