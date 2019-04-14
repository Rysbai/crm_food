from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from app.serializers.user import (
    RegistrationSerializer, LoginSerializer, UserSerializer, RoleSerializer
)
from app.models.user import Role, User
from app.renderers.user_renderer import UserJSONRenderer


class RoleView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get(self, request, *args, **kwargs):

        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        role_id = request.data.get('role_id', None)

        if role_id is None:
            raise ParseError("role_id field is required")

        try:
            role = self.queryset.get(id=role_id)
        except Role.DoesNotExist:
            raise Http404
        else:
            role.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        self.renderer_classes = JSONRenderer

        user_id = request.data.get('user_id', None)

        try:
            user = self.queryset.get(id=user_id)
        except User.DoesNotExist:
            raise Http404
        else:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    queryset = User.objects.all()


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


