from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import authentication
from .models import Token
from .serializers import (
    ObtainAuthTokenByAuthenticationSerializer, ObtainAuthTokenSerializer,
    RenewAuthTokenSerializer, TokenCreatedSerializer, TokenSerializer,
)


class AuthTokenView(APIView):
    """
    View to list available auth tokens and obtain them

    * Requires authentication
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=TokenSerializer(many=True),
    )
    def get(self, request):
        """
        Show all tokens for the current user.
        """
        queryset = Token.objects.filter(user=request.user)
        serializer = TokenSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ObtainAuthTokenSerializer,
        responses=TokenCreatedSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Obtain a new Token if already authenticated.
        """
        serializer = ObtainAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = Token.objects.create(
            user=request.user,
            application=serializer.validated_data['application'],
            expiring=serializer.validated_data.get('expiring'),
            renewable=serializer.validated_data['renewable'],
        )
        return Response({'token': token.key})


class AuthTokenDetailView(APIView):
    """
    View to revoke auth tokens

    * Requires authentication
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            204: None,
            404: None,
        },
    )
    def delete(self, request, *args, **kwargs):
        try:
            Token.objects.get(
                user=request.user,
                id=kwargs.get("id"),
            ).delete()
            return Response({"detail": "OK"})
        except ObjectDoesNotExist:
            raise NotFound


class ObtainAuthTokenWithCredentialsView(APIView):
    """
    View to obtain an authentication token with username/password
    """

    authentication_classes = []

    @extend_schema(
        request=ObtainAuthTokenByAuthenticationSerializer,
        responses=TokenCreatedSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = ObtainAuthTokenByAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = Token.objects.create(
            user=serializer.validated_data['user'],
            application=serializer.validated_data['application'],
            expiring=serializer.validated_data.get('expiring'),
            renewable=serializer.validated_data['renewable'],
        )
        return Response({'token': token.key})


class RenewAuthTokenView(APIView):
    """
    View to renew the token currently logged in with.

    * Requires authentication with renewable token.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RenewAuthTokenSerializer,
        responses=TokenCreatedSerializer
    )
    def post(self, request, *args, **kwargs):
        if request.auth.renewable:
            serializer = RenewAuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = Token.objects.create(
                user=request.user,
                application=request.auth.application,
                expiring=serializer.validated_data.get('expiring'),
                renewable=serializer.validated_data['renewable'],
            )
            request.auth.delete()
            return Response({'token': token.key})
        else:
            raise PermissionDenied('This API endpoint can only be used when authenticating with a renewable token')
