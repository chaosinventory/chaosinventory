from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...models import OIDCAccessToken, OIDCRefreshToken


class OIDCUserRevocationSerializer(serializers.Serializer):
    token_id = serializers.CharField(label="Token ID")

    def validate(self, attrs):
        token_jti = attrs.get('token_id')

        try:
            token = OIDCAccessToken.objects.get(
                jti=token_jti,
                user=self.context['request'].user
            )
        except ObjectDoesNotExist:
            try:
                token = OIDCRefreshToken.objects.get(
                    jti=token_jti,
                    user=self.context['request'].user
                )
            except ObjectDoesNotExist:
                raise serializers.ValidationError('Token ID is wrong')
        if not token.is_valid():
            raise serializers.ValidationError('Token ID is wrong')
        attrs['token'] = token
        return attrs


class OIDCUserRevocationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OIDCUserRevocationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['token'].revoke()
        return Response({"detail": "OK"})
