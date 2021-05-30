from base64 import urlsafe_b64encode
from hashlib import sha256

from ..models import OIDCGrant
from .exceptions import OIDCPKCEException


class OIDCPKCE:
    def __init__(self, request_parameters):
        self.request_type = None
        self.code_challenge = None
        self.code_verifier = None
        if request_parameters.get('code_challenge') is not None:
            self.request_type = 'authorize'
            self.code_challenge = request_parameters.get('code_challenge')
        elif request_parameters.get('code_verifier') is not None:
            self.request_type = 'token'
            self.code_verifier = request_parameters.get('code_verifier')
        else:
            raise OIDCPKCEException("Not a valid PKCE request.")

        if self.code_challenge is not None:
            self.code_challenge_method = request_parameters.get('code_challenge_method')
            if self.code_challenge_method is None:
                self.code_challenge_method = 'plain'
            self.code_challenge_method = self.code_challenge_method.lower()
            if self.code_challenge_method not in ('plain', 's256'):
                raise OIDCPKCEException("'code_challenge_method' must be 's256' or 'plain'.")
        else:
            self.code_challenge_method = None

    def verify_challenge(self, grant: OIDCGrant) -> bool:
        if not self.request_type == 'token':
            raise OIDCPKCEException("Challenge can only be verified in token requests.")

        if grant.code_challenge is None or grant.code_challenge_method is None:
            raise OIDCPKCEException("This grant can not be used for PKCE.")

        comparable_code_verifier = self.code_verifier
        if grant.code_challenge_method == 's256':
            # hash
            comparable_code_verifier = urlsafe_b64encode(
                sha256(comparable_code_verifier.encode()).digest()
            ).decode().rstrip('=')

        return grant.code_challenge == comparable_code_verifier

    @staticmethod
    def is_pkce(request_parameters) -> bool:
        return request_parameters.get('code_challenge') is not None or request_parameters.get(
            'code_verifier') is not None
