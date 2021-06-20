from uuid import UUID

import jwt
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chaosinventory.authentication.models import (
    OIDCAccessToken, OIDCRefreshToken,
)
from chaosinventory.authentication.oidc.authentication import (
    OIDCApplicationBasicAuthentication,
    OIDCApplicationRequestBodyAuthentication,
)
from chaosinventory.authentication.oidc.exceptions import OIDCJWTException
from chaosinventory.authentication.oidc.jwt import OIDCTokenJWT


class OIDCRevocationSerializer(serializers.Serializer):
    token = serializers.CharField(label="Token")

    def validate(self, attrs):
        token = attrs.get('token')

        try:
            decoded_jwt = jwt.decode(
                token,
                options={
                    "verify_signature": False,
                    "verify_aud": False,
                })
        except jwt.exceptions.InvalidTokenError:
            raise serializers.ValidationError("The given token is invalid.")
        try:
            if decoded_jwt['typ'] == 'Bearer':
                validated_token = OIDCTokenJWT.validate_token(token, "Bearer", OIDCAccessToken)
            elif decoded_jwt['typ'] == "Refresh":
                validated_token = OIDCTokenJWT.validate_token(token, "Refresh", OIDCRefreshToken)
            else:
                raise serializers.ValidationError("The given token is not revocable.")
        except OIDCJWTException as e:
            raise serializers.ValidationError(e)
        if UUID(validated_token['parsed_token']['aud']) != self.context['request'].user.pk:
            raise serializers.ValidationError("The given token is not issued to the authenticated application.")

        attrs['token'] = validated_token
        return attrs


class OIDCRevocationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [OIDCApplicationBasicAuthentication, OIDCApplicationRequestBodyAuthentication]
    serializer_class = OIDCRevocationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['token']['db_token'].revoke()
        return Response({"detail": "OK"})
