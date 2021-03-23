import secrets

from django.contrib.auth.models import User
from django.db import models


class Token(models.Model):
    key = models.CharField(
        max_length=40,
        primary_key=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    application = models.CharField(max_length=255)
    expiring = models.DateTimeField(
        null=True,
        blank=True)
    renewable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_token()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_token(cls):
        token = secrets.token_hex(32)
        while cls.objects.filter(key=token).count() > 0:
            token = secrets.token_hex(32)
        return token
