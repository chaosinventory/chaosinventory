import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from chaosinventory.authentication.models import Token, User


class ApiTestCase(TestCase):
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

    # TODO: Deduplicate
    # Currently, this part is the same as in test_token.py
    # but it would be nice, if we could deduplicate a bit
    def assertValidJson(self, content: str):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            self.fail('Failed to parse JSON')

    def api_call(self, path: str, payload: dict = None, token: str = None, method: str = 'get',
                 decode_json: bool = True):
        if payload is None:
            payload = {}

        headers = {}
        if token is not None:
            headers['HTTP_AUTHORIZATION'] = f'Token {token}'

        if method == 'get':
            response = self.client.get(
                path,
                payload,
                **headers,
            )
        elif method == 'post':
            response = self.client.post(
                path,
                payload,
                **headers,
            )
        else:
            raise ValueError('method must be either get or post')

        if decode_json:
            self.assertValidJson(response.content)
            return response, json.loads(response.content)
        else:
            return response, response.content

    # End of the copied part

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
