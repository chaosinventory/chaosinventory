# inspired by rest_framework.authentication.TokenAuthentication
from typing import Optional

from rest_framework import authentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from ..models import OIDCAccessToken
from . import exceptions
from .exceptions import OIDCJWTException
from .views.token import OIDCTokenJWT


class OIDCAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple]:
        auth_header = get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != "Bearer".lower().encode():
            return None

        if len(auth_header) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth_header[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        try:
            oidc_token_validation = OIDCTokenJWT.validate_token(
                token=token,
                token_type="Bearer",
                token_db_model=OIDCAccessToken
            )
        except OIDCJWTException as e:
            raise AuthenticationFailed(e)
        return oidc_token_validation['user'], oidc_token_validation['parsed_token']

    def authenticate_header(self, request):
        return "Bearer"
