import urllib.parse
from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import (
    HttpRequest, HttpResponse, HttpResponseBadRequest, QueryDict,
)
from django.shortcuts import redirect
from django.views import View

from ...models import OIDCApplication, OIDCGrant
from ..exceptions import OIDCPKCEException, OIDCRequestParsingException
from ..pkce import OIDCPKCE


class OIDCAuthorizeRequest:
    SCOPE_CLAIMS = {
        'openid': [
            'sub',
            'iss',
            'aud',
            'exp',
            'iat'
        ],
        'profile': [
            'name',
            'given_name',
            'family_name',
            'preferred_username'
        ],
        'email': [
            'email',
            'email_verified'
        ]
    }

    def __init__(self, request_parameters: QueryDict):
        self._request_parameters = request_parameters
        self.validate_request_parameters()

        self.client_id = request_parameters['client_id']
        self.response_type = request_parameters['response_type']
        self.response_mode = request_parameters.get('response_mode', 'query')
        self.scope = request_parameters['scope']
        self.redirect_uri = request_parameters.get('redirect_uri')
        self.nonce = request_parameters.get('nonce')
        self.application = None
        self.code_challenge = None
        self.code_challenge_method = None

        self.validate_fields()
        self.claims = self.parse_scope_to_claims()
        self.verify_application()

    def validate_request_parameters(self):
        for field in ('client_id', 'scope', 'response_type'):
            if field not in self._request_parameters:
                raise OIDCRequestParsingException(f"'{field}' is missing in the request")

    def validate_fields(self):
        if self.response_type != 'code':
            raise OIDCRequestParsingException("'response_type' is not 'code'. Currently is only the Authorization "
                                              "code flow supported.")
        if self.response_mode not in ('query', 'fragment'):
            raise OIDCRequestParsingException(
                "'response_mode' is not 'query' or 'fragment'. Currently only these are supported.")
        if 'openid' not in self.scope:
            raise OIDCRequestParsingException("'openid' currently must be in the 'scope'.")

        # TODO: deduplicate
        try:
            self.application: OIDCApplication = OIDCApplication.objects.get(client_id=self.client_id)
        except (ObjectDoesNotExist, ValidationError):
            raise OIDCRequestParsingException("'client_id' is invalid or has an invalid format.")

        if self.redirect_uri is None:
            if self.application.default_redirect_uri is None:
                raise OIDCRequestParsingException("'redirect_uri' is missing in the request")
            else:
                self.redirect_uri = self.application.default_redirect_uri
        if not self.application.is_redirect_uri_allowed(self.redirect_uri):
            raise OIDCRequestParsingException("The given redirect URI is not allowed in the application.")

    def parse_scope_to_claims(self) -> List[str]:
        claims = []
        for scope in self.scope.split(" "):
            if scope not in self.SCOPE_CLAIMS:
                raise OIDCRequestParsingException(f"The scope part {scope} is not supported.")
            claims += self.SCOPE_CLAIMS[scope]
        if self.nonce is not None:
            claims += ['nonce']
        return claims

    def verify_application(self):  # TODO: Deduplicate
        if self.application.access_type == "confidential":
            pass
        elif self.application.access_type == 'public':  # PKCE
            try:
                oidcpkce_flow = OIDCPKCE(self._request_parameters)
            except OIDCPKCEException:
                raise OIDCRequestParsingException("'code_challenge' is missing in the request or is invalid.")
            self.code_challenge = oidcpkce_flow.code_challenge
            self.code_challenge_method = oidcpkce_flow.code_challenge_method

        else:  # This exception should _never_ occur, thus the error message is quite not that serious.
            raise OIDCRequestParsingException("Uhm somehow the DB validations didn't work.")


class OIDCAuthorizeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        # TODO: Authorize (Allow xyz to access abc) page
        try:
            parsed_request = OIDCAuthorizeRequest(request.GET)
        except OIDCRequestParsingException as e:
            return HttpResponseBadRequest(e)
        application = OIDCApplication.objects.get(client_id=parsed_request.client_id)
        grant = OIDCGrant.objects.create(
            user=request.user,
            application=application,
            redirect_uri=parsed_request.redirect_uri,
            claims=parsed_request.claims,
            code_challenge=parsed_request.code_challenge,
            code_challenge_method=parsed_request.code_challenge_method,
            nonce=parsed_request.nonce
        )

        response_parameters = urllib.parse.urlencode({'code': grant.code})

        redirect_url = ""
        if parsed_request.response_mode == 'query':
            redirect_url = parsed_request.redirect_uri + "?" + response_parameters
        elif parsed_request.response_mode == 'fragment':
            redirect_url = parsed_request.redirect_uri + "#" + response_parameters
        return redirect(redirect_url)
