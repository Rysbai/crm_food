from django.contrib.auth import authenticate
from rest_framework import serializers

from app.models.user import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class RegistrationSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role.id'
    )
    password = serializers.CharField(
        max_length=128, 
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['role_id', 'name', 'surname', 'email', 'username', 'created_at', 'password', 'token']
        read_only_fields = ('create_at', 'token')

    def create(self, validated_data):
        return User.objects.create_user(
            role=validated_data.pop('role')['id'],
            **validated_data
        )


class LoginSerializer(serializers.Serializer):
    role_id = serializers.IntegerField(
        source='role.id',
        read_only=True
    )
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This user has been deactivated."
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('role_id', 'name', 'surname', 'email', 'username', 'created_at', 'password', 'token')
        read_only_fields = ('token',)

    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
