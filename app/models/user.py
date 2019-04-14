import jwt

from django.db import models
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from app.exceptions import message_constants


class UserManager(BaseUserManager):
    def create_user(self, role, name, surname, username, email, phone, password=None):
        if username is None:
            raise TypeError(message_constants.USERS_MUST_HAVE_AN_USERNAME)

        if email is None:
            raise TypeError(message_constants.USERS_MUST_HAVE_AN_EMAIL)

        if phone is None:
            raise TypeError(message_constants.USERS_MUST_HAVE_A_PHONE)

        user = self.model(
            role=role,
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            name=name,
            surname=surname
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError(message_constants.SUPER_USERS_MUST_HAVE_A_PASSWORD)

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Role(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    name = models.CharField(db_index=True, max_length=255)
    surname = models.CharField(db_index=True, max_length=255)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    phone = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.name + " " + self.surname

    def get_short_name(self):
        return self.name

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
