from django.utils import timezone
from rest_framework import authentication, exceptions

from . import models


class TokenAuthentication(authentication.TokenAuthentication):
    model = models.Token

    # extended version of rest_framework.authentication.TokenAuthentication.authenticate_credentials
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if token.expiring is not None and token.expiring < timezone.now():
            raise exceptions.AuthenticationFailed('Expired token.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)
