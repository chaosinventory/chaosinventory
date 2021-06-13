from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from chaosinventory.authentication.models import Token, User

from ..mixins import ApiTestMixin


class ApiTestCase(TestCase, ApiTestMixin):
    def setUp(self) -> None:
        self.user_password: str = 'password'
        self.user: User = get_user_model().objects.create(
            username=self.__class__.__name__,
            first_name='Demo',
            last_name='User',
            email='user@example.org',
        )
        self.db_token = Token()
        self.db_token.user = self.user
        self.db_token.application = self.__class__.__name__
        self.db_token.save()
        self.token = self.db_token.key

    def test_api_tag(self):
        response, content = self.api_call(
            reverse('tag-list'),
            token=self.token,
        )
        self.assertEqual(response.status_code, 200)
        response, content = self.api_call(
            reverse('tag-list'),
            token=self.token,
            payload={'name': 'ABC', },
            method='post',
        )
        self.assertEqual(response.status_code, 201)
