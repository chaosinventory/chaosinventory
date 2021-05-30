from typing import Dict, List, Optional, Type, Union

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.utils import timezone

from ..models.oidc import AbstractOIDCToken
from .exceptions import OIDCJWTException


class OIDCTokenJWT:
    def __init__(
            self,
            request: HttpRequest,
            parsed_request,  # here should be a type hint to OIDCTokenRequest, but then we would have a circular import
            db_token: AbstractOIDCToken,
            claims: List[str],
            type: str):
        self._request = request
        self._parsed_request = parsed_request
        self._db_token = db_token
        self.type = type
        self.claims = claims
        self.expiry = db_token.expiry
        self.payload = self.create_jwt_payload()

    def resolve_claim(self, claim: str) -> Optional[Union[str, int]]:
        if claim == 'jti':
            return str(self._db_token.jti)
        elif claim == 'typ':
            return self.type
        elif claim == 'sub':
            return str(self._parsed_request.grant.user.pk)
        elif claim == 'iss':
            return f"https://{self._request.META['HTTP_HOST']}"
        elif claim == 'aud':
            return self._parsed_request.client_id
        elif claim == 'exp':
            return int(self.expiry.timestamp())
        elif claim == 'iat':
            return int(timezone.now().timestamp())
        elif claim == 'nonce':
            try:
                return self._parsed_request.grant.nonce
            except AttributeError:
                return None
        elif claim == 'name':
            user = self._parsed_request.grant.user
            return f'{user.first_name} {user.last_name}'
        elif claim == 'given_name':
            return self._parsed_request.grant.user.first_name
        elif claim == 'family_name':
            return self._parsed_request.grant.user.last_name
        elif claim == 'preferred_username':
            return self._parsed_request.grant.user.username
        elif claim == 'email':
            return self._parsed_request.grant.user.email
        elif claim == 'email_verified':
            return False
        else:
            raise OIDCJWTException(f"The claim {claim} couldn't be parsed")

    def create_jwt_payload(self) -> Dict[str, Union[str, int]]:
        claims = ['jti', 'typ'] + self.claims
        payload = {}
        for claim in claims:
            claim_content = self.resolve_claim(claim)
            if claim_content is not None:
                payload[claim] = claim_content
        return payload

    @property
    def jwt(self) -> str:
        return jwt.encode(
            payload=self.payload,
            key=settings.OIDC_JWT_PRIVATE_KEY,
            algorithm=settings.OIDC_JWT_KEY_ALGORITHM
        )

    @staticmethod
    def validate_token(
            token: str,
            token_type: str,
            token_db_model: Type[AbstractOIDCToken],
            audience: Optional[str] = None):
        try:
            jwt_token = jwt.decode(
                jwt=token,
                key=settings.OIDC_JWT_PUBLIC_KEY,
                algorithms=settings.OIDC_JWT_KEY_ALGORITHM,
                audience=audience,
                options={
                    "verify_aud": audience is not None
                }
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise OIDCJWTException(f"The {token_type} token is expired.")
        except jwt.exceptions.InvalidAudienceError:
            raise OIDCJWTException(f"The client_secret doesn't fit to the {token_type} token.")
        except jwt.exceptions.PyJWTError:
            raise OIDCJWTException(f"The {token_type} token is invalid.")
        if jwt_token.get('typ') != token_type:
            raise OIDCJWTException(f"The given token in the 'Authorization' header is not an {token_type} token")
        try:
            user = get_user_model().objects.get(pk=jwt_token['sub'])
        except ObjectDoesNotExist:
            raise OIDCJWTException(f"The {token_type} token is invalid.")
        try:
            db_jwt_token = token_db_model.objects.get(jti=jwt_token['jti'])
        except ObjectDoesNotExist:
            raise OIDCJWTException(f"The {token_type} token is invalid.")
        if not db_jwt_token.is_valid():
            raise OIDCJWTException(f"The {token_type} token is invalid.")
        return {
            "user": user,
            "parsed_token": jwt_token,
            "db_token": db_jwt_token
        }
