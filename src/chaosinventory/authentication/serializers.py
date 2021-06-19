from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Token


class ObtainAuthTokenSerializer(serializers.Serializer):
    application = serializers.CharField(label="Application Name")
    expiring = serializers.DateTimeField(
        label="Date/Time when token expires",
        required=False,
    )
    renewable = serializers.BooleanField(
        label="Renewability of token",
        default=True,
    )


class ObtainAuthTokenByAuthenticationSerializer(ObtainAuthTokenSerializer):
    username = serializers.CharField(label="Username")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                'Username and/or password is wrong',
                code='authorization',
            )

        attrs['user'] = user
        return attrs


class RenewAuthTokenSerializer(serializers.Serializer):
    expiring = serializers.DateTimeField(
        label="Date/Time when token expires",
        required=False,
    )
    renewable = serializers.BooleanField(
        label="Renewability of token",
        default=True,
    )


class TokenSerializer(serializers.ModelSerializer):
    token_beginning = serializers.SerializerMethodField()

    def get_token_beginning(self, obj) -> str:
        return obj.key[:6]

    class Meta:
        model = Token
        fields = [
            'id',
            'token_beginning',
            'application',
            'created',
            'expiring',
            'renewable',
        ]


class TokenCreatedSerializer(serializers.Serializer):
    token = serializers.CharField()
