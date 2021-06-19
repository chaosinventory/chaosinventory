from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import OIDCAccessToken
from .. import authentication


class OIDCUserInfoView(APIView):
    authentication_classes = [authentication.OIDCAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token_jti = request.auth['jti']
        db_token = OIDCAccessToken.objects.get(jti=token_jti)
        claims = db_token.source_refresh_token.claims
        response = {}
        for claim in claims:
            resolved_claim = self.resolve_claim(claim, request.user, token_jti, request)
            if resolved_claim is not None:
                response[claim] = resolved_claim
        return Response(response)

    def post(self, request):
        return self.get(request)

    @staticmethod
    def resolve_claim(claim, user, token_jti, request):
        # TODO: deduplicate or implement in a more efficient way (can be done later)
        if claim == 'sub':
            return str(user.pk)
        elif claim == 'iss':
            return f"https://{request.META['HTTP_HOST']}"
        elif claim == 'aud':
            return token_jti
        elif claim == 'name':
            return f'{user.first_name} {user.last_name}'
        elif claim == 'given_name':
            return user.first_name
        elif claim == 'family_name':
            return user.last_name
        elif claim == 'preferred_username':
            return user.username
        elif claim == 'email':
            return user.email
        elif claim == 'email_verified':
            return False
        # the following claims shouldn't be present in the response
        elif claim in ('exp', 'iat'):
            return None
        else:
            raise APIException(f"The claim {claim} couldn't be parsed")
