from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import (
    HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse, QueryDict,
)
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ...models import (
    OIDCAccessToken, OIDCApplication, OIDCGrant, OIDCIDToken, OIDCRefreshToken,
)
from ..exceptions import (
    OIDCJWTException, OIDCPKCEException, OIDCRequestParsingException,
)
from ..jwt import OIDCTokenJWT
from ..pkce import OIDCPKCE


class OIDCTokenRequest:
    def __init__(self, request_parameters: QueryDict):
        self.validate_request_parameters(request_parameters)

        self._request_parameters = request_parameters

        self.client_id = request_parameters['client_id']
        self.redirect_uri = request_parameters.get('redirect_uri')
        self.grant_type = request_parameters['grant_type']
        self.client_secret = request_parameters.get('client_secret')
        self.code = request_parameters.get('code')
        self.raw_refresh_token = request_parameters.get('refresh_token')
        self.jwt_refresh_token = None
        self.application = None
        self.grant = None

        self.validate_fields()
        self.verify_grant()
        self.verify_application()

    @staticmethod
    def validate_request_parameters(request_parameters: QueryDict):
        for field in ('client_id', 'grant_type'):
            if field not in request_parameters:
                raise OIDCRequestParsingException(f"'{field}' is missing in the request")

    def validate_fields(self):
        # TODO: deduplicate
        try:
            self.application: OIDCApplication = OIDCApplication.objects.get(client_id=self.client_id)
        except (ObjectDoesNotExist, ValidationError):
            raise OIDCRequestParsingException("'client_id' is invalid or has an invalid format.")

    def verify_grant(self):
        if self.grant_type == 'authorization_code':
            if self.code is None:
                raise OIDCRequestParsingException("'code' is missing in the request")
            try:
                grant: OIDCGrant = OIDCGrant.objects.get(
                    code=self.code,
                    application=self.application,
                )
            except ObjectDoesNotExist:
                raise OIDCRequestParsingException("There is no valid grant with the given 'code'.")
            if not grant.is_valid():
                raise OIDCRequestParsingException("There is no valid grant with the given 'code'.")
            self.grant = grant

            if self.application.default_redirect_uri is None:
                if self.redirect_uri is None:
                    raise OIDCRequestParsingException("'redirect_uri' is missing in the request")
                else:
                    if not self.application.is_redirect_uri_allowed(self.redirect_uri):
                        raise OIDCRequestParsingException("The given redirect URI is not allowed in the application.")
            else:
                self.redirect_uri = self.application.default_redirect_uri

            if self.redirect_uri != grant.redirect_uri:
                raise OIDCRequestParsingException(
                    "The given redirect URI doesn't match the redirect URI used to authorize.")

        elif self.grant_type == 'refresh_token':
            if self.raw_refresh_token is None:
                raise OIDCRequestParsingException("'refresh_token' is missing in the request")
            try:
                refresh_token_validation = OIDCTokenJWT.validate_token(
                    token=self.raw_refresh_token,
                    token_type="Refresh",
                    token_db_model=OIDCRefreshToken,
                    audience=self.client_id
                )
            except OIDCJWTException as e:
                raise OIDCRequestParsingException(e)
            if refresh_token_validation['db_token'].application != self.application:
                raise OIDCRequestParsingException("The 'refresh_token' is invalid.")
            self.grant = refresh_token_validation['db_token']  # In the spec, this is a grant too.

        else:
            raise OIDCRequestParsingException("The 'grant_type' must be 'authorization_code' or 'refresh_token'.")

    def verify_application(self):
        if self.application.access_type == "confidential":
            if self.client_secret is None:
                raise OIDCRequestParsingException("'client_secret' is missing in the request")
            if not self.application.check_client_secret(self.client_secret):
                raise OIDCRequestParsingException(
                    "The provided client secret doesn't match the client secret of the application.")

        elif self.application.access_type == 'public':  # PKCE
            if self.grant_type == 'authorization_code':
                try:
                    oidcpkce_flow = OIDCPKCE(self._request_parameters)
                except OIDCPKCEException:
                    raise OIDCRequestParsingException("'code_verifier' is missing in the request.")
                if not oidcpkce_flow.verify_challenge(self.grant):
                    raise OIDCRequestParsingException("'code_verifier' is invalid.")

        else:  # This exception should _never_ occur, thus the error message is quite not that serious.
            raise OIDCRequestParsingException("Uhm somehow the DB validations didn't work.")


@method_decorator(csrf_exempt, name='dispatch')
class OIDCTokenView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            parsed_request = OIDCTokenRequest(request.POST)
        except OIDCRequestParsingException as e:
            return HttpResponseBadRequest(e)

        # Refresh token
        refresh_token_expires_in = timedelta(days=settings.OIDC_REFRESH_TOKEN_EXPIRY_DAYS)
        refresh_token_expiry = timezone.now() + refresh_token_expires_in
        db_refresh_token: OIDCRefreshToken = OIDCRefreshToken.objects.create(
            user=parsed_request.grant.user,
            application=parsed_request.grant.application,
            expiry=refresh_token_expiry,
            claims=parsed_request.grant.claims,
        )
        refresh_jwt = OIDCTokenJWT(
            request=request,
            parsed_request=parsed_request,
            db_token=db_refresh_token,
            claims=['sub', 'iss', 'aud', 'exp', 'iat'],
            type="Refresh"
        )

        # Access token
        access_token_expires_in = timedelta(minutes=settings.OIDC_ACCESS_TOKEN_EXPIRY_MINUTES)
        access_token_expiry = timezone.now() + access_token_expires_in
        db_access_token: OIDCAccessToken = OIDCAccessToken.objects.create(
            user=parsed_request.grant.user,
            expiry=access_token_expiry,
            source_refresh_token=db_refresh_token
        )
        access_jwt = OIDCTokenJWT(
            request=request,
            parsed_request=parsed_request,
            db_token=db_access_token,
            claims=['sub', 'iss', 'aud', 'exp', 'iat'],
            type="Bearer"
        )

        # ID token
        id_token_expires_in = timedelta(minutes=settings.OIDC_ID_TOKEN_EXPIRY_MINUTES)
        id_token_expiry = timezone.now() + id_token_expires_in
        db_id_token: OIDCIDToken = OIDCIDToken.objects.create(
            user=parsed_request.grant.user,
            expiry=id_token_expiry,
            source_refresh_token=db_refresh_token
        )
        id_jwt = OIDCTokenJWT(
            request=request,
            parsed_request=parsed_request,
            db_token=db_id_token,
            claims=parsed_request.grant.claims,
            type="Id"
        )
        parsed_request.grant.revoke()
        return JsonResponse({
            "access_token": access_jwt.jwt,
            "expires_in": int(access_token_expires_in.total_seconds()),
            "refresh_expires_in": int(refresh_token_expires_in.total_seconds()),
            "refresh_token": refresh_jwt.jwt,
            "id_token": id_jwt.jwt,
        })
