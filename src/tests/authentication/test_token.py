import json
from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from chaosinventory.authentication.models import Token, User


def get_db_token(key):
    return Token.objects.get(key=key)


class TokenTestCase(TestCase):
    def setUp(self) -> None:
        self.user_password: str = 'password'
        self.user: User = get_user_model()()
        self.user.username = 'test'
        self.user.first_name = 'Demo'
        self.user.last_name = 'User'
        self.user.email = 'user@example.org'
        self.user.set_password(self.user_password)
        self.user.save()

    def obtain_token(self, username: str = None, password: str = None, application: str = None,
                     expiring: Optional[datetime] = None, renewable: bool = True):
        payload = {
            'username': self.user.username if username is None else username,
            'password': self.user_password if password is None else password,
            'application': self.__class__.__name__ if application is None else application,
            'renewable': renewable,
        }

        if expiring is not None:
            payload['expiring'] = expiring

        return self.client.post(
            '/api/authentication/token/credentials',
            payload,
        )

    def get_token(self, response=None, **kwargs):
        if response is None:
            response = self.obtain_token(**kwargs)

        return json.loads(response.content)['token']

    def api_call(self, path: str, payload: dict = None, token: str = None, method: str = 'get'):
        if payload is not None:
            payload = {}

        headers = {}
        if token is not None:
            headers['HTTP_AUTHORIZATION'] = f'Token {token}'

        if method == 'get':
            return self.client.get(
                path,
                payload,
                **headers,
            )
        elif method == 'post':
            return self.client.post(
                path,
                payload,
                **headers,
            )
        else:
            raise ValueError('method mus be either get or post')

    def test_obtain_token_json(self):
        response = self.obtain_token()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        try:
            token = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail('Failed to parse JSON')
        self.assertTrue('token' in token)

    def test_token_in_db(self):
        token = self.get_token()
        try:
            self.user.token_set.filter(key=token).get()
        except ObjectDoesNotExist:
            self.fail('No matching token was found for this user in the database.')

    def _test_renewable_token(self, renewable):
        token = self.get_token(renewable=renewable)
        db_token: Token = get_db_token(key=token)
        self.assertEqual(db_token.renewable, renewable)

    def test_token_renewable(self):
        self._test_renewable_token(True)
        self._test_renewable_token(False)
        # TODO: Actually try to renew the token

    def test_token_api_auth(self):
        self.assertEqual(
            self.api_call(reverse('tag-list')).status_code,
            401,
        )
        token = self.get_token()
        self.assertEqual(
            self.api_call(
                reverse('tag-list'),
                token=token[0:-10],
            ).status_code,
            401
        )
        self.assertEqual(
            self.api_call(
                reverse('tag-list'),
                token=token,
            ).status_code,
            200,
        )
