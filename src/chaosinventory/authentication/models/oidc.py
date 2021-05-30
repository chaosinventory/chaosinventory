import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone

from ..oidc.exceptions import OIDCRequestParsingException


def _generate_secret():
    return secrets.token_hex(32)


class OIDCApplication(models.Model):
    ACCESS_TYPES = [
        ('public', 'Public'),
        ('confidential', 'Confidential'),
    ]
    client_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    description = models.TextField(
        null=True,
        blank=True)
    client_secret = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    _client_secret = None
    access_type = models.CharField(
        max_length=255,
        choices=ACCESS_TYPES,
        default='confidential'
    )
    redirect_uris = models.JSONField()
    default_redirect_uri = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.client_secret is None:
            self.generate_new_client_secret(save=False)
        return super().save(*args, **kwargs)

    def generate_new_client_secret(self, save=True) -> str:
        new_client_secret = _generate_secret()
        self.client_secret = make_password(new_client_secret)
        if save:
            self.save(update_fields=["client_secret"])
        self._client_secret = new_client_secret
        return new_client_secret

    # modified version from django.contrib.auth.base_user
    def check_client_secret(self, raw_client_secret):
        """
        Returns a boolean of whether the raw_client_secret was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_client_secret):
            self.client_secret = make_password(raw_client_secret)
            # Password hash upgrades shouldn't be considered password changes.
            self.save(update_fields=["client_secret"])

        return check_password(raw_client_secret, self.client_secret, setter)

    def is_redirect_uri_allowed(self, redirect_uri):
        # TODO: Allow usage of * in `redirect_uris`. For example `https://example.org/*`
        try:
            URLValidator()(redirect_uri)
        except ValidationError:
            raise OIDCRequestParsingException("'redirect_uri' has an invalid format.")

        return redirect_uri in self.redirect_uris


class OIDCGrant(models.Model):
    code = models.CharField(
        max_length=64,
        unique=True,
        primary_key=True,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )
    application = models.ForeignKey(
        OIDCApplication,
        on_delete=models.CASCADE,
        editable=False,
    )
    expiry = models.DateTimeField(
        editable=False
    )
    redirect_uri = models.CharField(
        max_length=255,
        editable=False,
    )
    nonce = models.CharField(
        max_length=255,
        editable=False,
        null=True,
        blank=True
    )
    claims = models.JSONField(
        editable=False,
    )
    code_challenge = models.CharField(
        max_length=128,
        editable=False,
        null=True,
        blank=True
    )  # PKCE
    code_challenge_method = models.CharField(
        max_length=5,
        editable=False,
        null=True,
        blank=True,
        choices=(('s256', 'SHA256'), ('plain', 'Plain (insecure)'),),
    )  # PKCE
    revoked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expiry:
            self.expiry = timezone.now() + timedelta(minutes=settings.OIDC_GRANT_EXPIRY_MINUTES)
        return super().save(*args, **kwargs)

    @classmethod
    def generate_code(cls):
        code = _generate_secret()
        while cls.objects.filter(code=code).count() > 0:
            code = _generate_secret()
        return code

    def is_valid(self) -> bool:
        return (self.expiry > timezone.now()) and (not self.revoked)

    def revoke(self):
        self.revoked = True
        self.save()


class AbstractOIDCToken(models.Model):
    class Meta:
        abstract = True

    jti = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )
    expiry = models.DateTimeField(editable=False)
    revoked = models.DateTimeField(
        null=True,
        blank=True
    )

    def revoke(self):
        self.revoked = timezone.now()
        self.save()

    def is_valid(self) -> bool:
        return (self.expiry > timezone.now()) and (self.revoked is None)


class OIDCRefreshToken(AbstractOIDCToken):
    application = models.ForeignKey(
        OIDCApplication,
        on_delete=models.CASCADE,
        editable=False,
    )

    claims = models.JSONField(
        editable=False,
    )

    def revoke(self):
        self.revoked = timezone.now()
        if self.access_token:
            self.access_token.revoke()
        if self.id_token:
            self.id_token.revoke()
        self.save()


class OIDCAccessToken(AbstractOIDCToken):
    source_refresh_token = models.OneToOneField(
        OIDCRefreshToken,
        on_delete=models.CASCADE,
        related_name="access_token",
        editable=False,
    )


class OIDCIDToken(AbstractOIDCToken):
    source_refresh_token = models.OneToOneField(
        OIDCRefreshToken,
        on_delete=models.CASCADE,
        related_name="id_token",
        editable=False,
    )
