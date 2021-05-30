import json
from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

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
            raise ValueError('method mus be either get or post')

        if decode_json:
            self.assertValidJson(response.content)
            return response, json.loads(response.content)
        else:
            return response, response.content

    def validate_token_against_api(self, token):
        response, response_content = self.api_call('/api/authentication/token/', token=token)
        self.assertEqual(response.status_code, 200)
        return response

    def test_obtain_token_json(self):
        response = self.obtain_token()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        token = self.assertValidJson(response.content)
        self.assertTrue('token' in token)

    def test_user_token_in_db(self):
        token = self.get_token()
        try:
            self.user.token_set.filter(key=token).get()
        except ObjectDoesNotExist:
            self.fail('No matching token was found for this user in the database.')

    def validate_token_renewal(self, renewable):
        token = self.get_token(renewable=renewable)
        db_token: Token = get_db_token(key=token)
        self.assertEqual(db_token.renewable, renewable)
        new_token_response, new_token = self.api_call(
            '/api/authentication/token/renew',
            token=token,
            method='post'
        )
        if renewable:
            self.assertEqual(new_token_response.status_code, 200)
            self.validate_token_against_api(new_token['token'])
        else:
            self.assertEqual(new_token_response.status_code, 403)

    def test_token_renewable(self):
        self.validate_token_renewal(True)
        self.validate_token_renewal(False)

    def test_token_api_auth(self):
        self.assertEqual(
            self.api_call('/api/authentication/token/')[0].status_code,
            401,
        )
        token = self.get_token()
        self.assertEqual(
            self.api_call(
                '/api/authentication/token/',
                token='invalid',
            )[0].status_code,
            401
        )
        self.assertEqual(
            self.api_call(
                '/api/authentication/token/',
                token=token,
            )[0].status_code,
            200,
        )
