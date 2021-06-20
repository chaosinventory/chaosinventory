from typing import Optional

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import authentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from ..models import OIDCAccessToken, OIDCApplication
from . import exceptions
from .exceptions import OIDCJWTException
from .views.token import OIDCTokenJWT


def _validate_authorize_header(request: Request, header_name: str) -> Optional[str]:
    auth_header = get_authorization_header(request).split()

    if not auth_header or auth_header[0].lower() != header_name.lower().encode():
        return None

    if len(auth_header) == 1:
        msg = 'Invalid token header. No credentials provided.'
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth_header) > 2:
        msg = 'Invalid token header. Token string should not contain spaces.'
        raise exceptions.AuthenticationFailed(msg)

    try:
        return auth_header[1].decode()
    except UnicodeError:
        msg = 'Invalid Authorize header. Token string should not contain invalid characters.'
        raise exceptions.AuthenticationFailed(msg)


# inspired by rest_framework.authentication.TokenAuthentication
class OIDCAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple]:
        header_content = _validate_authorize_header(request, "Bearer")
        try:
            oidc_token_validation = OIDCTokenJWT.validate_token(
                token=header_content,
                token_type="Bearer",
                token_db_model=OIDCAccessToken
            )
        except OIDCJWTException as e:
            raise AuthenticationFailed(e)
        return oidc_token_validation['user'], oidc_token_validation['parsed_token']

    def authenticate_header(self, request):
        return "Bearer"


class OIDCApplicationBasicAuthentication(authentication.BasicAuthentication):
    def authenticate_credentials(self, client_id, client_secret, request=None):
        try:
            application: OIDCApplication = OIDCApplication.objects.get(
                client_id=client_id,
                access_type="confidential",
            )
        except (ObjectDoesNotExist, ValidationError):
            raise AuthenticationFailed("Application with given credentials not found "
                                       "or application has not access_type 'confidential'")
        if not application.check_client_secret(client_secret):
            raise AuthenticationFailed("Application with given credentials not found "
                                       "or application has not access_type 'confidential'")
        return application, None


class OIDCApplicationRequestBodyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request) -> Optional[tuple]:
        try:
            application = OIDCApplication.objects.get(client_id=request.data.get('client_id'))
        except (ObjectDoesNotExist, ValidationError):
            raise AuthenticationFailed("Application with given credentials not found")

        if application.access_type == "confidential":
            if request.data.get('client_secret') is None:
                raise AuthenticationFailed("'client_secret' is missing in the request")
            if not application.check_client_secret(request.data.get('client_secret')):
                raise AuthenticationFailed("Application with given credentials not found")
        return application, None
