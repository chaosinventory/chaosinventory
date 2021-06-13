import json
import uuid
from datetime import datetime, timedelta
from time import sleep
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from chaosinventory.authentication.models import Token, User

from ..mixins import ApiTestMixin


def get_db_token(key) -> Token:
    return Token.objects.get(key=key)


def create_user(**kwargs) -> User:
    password = None
    if 'password' in kwargs:
        password = kwargs.pop('password')

    default_user_data = {
        'username': uuid.uuid4(),
        'first_name': 'Demo',
        'last_name': 'User',
        'email': 'user@example.org',
    }
    user: User = get_user_model().objects.create(**{**default_user_data, **kwargs})

    if password is not None:
        user.set_password(password)
        user.save()

    return user


class TokenTestCase(TestCase, ApiTestMixin):
    def setUp(self) -> None:
        self.user_password: str = 'password'
        self.user = create_user(password=self.user_password)

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

    def validate_token_against_api(self, token: Optional[str] = None, expected_status_code: Optional[int] = 200):
        response, response_content = self.api_call('/api/authentication/token/', token=token)
        if expected_status_code is not None:
            self.assertEqual(response.status_code, expected_status_code)
        return response, response_content

    def test_obtain_token_json(self):
        response = self.obtain_token()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        token = self.assertValidJson(response.content)
        self.assertTrue('token' in token)

    def test_token_bad_password(self):
        response = self.obtain_token(password='')
        self.assertEqual(response.status_code, 400)
        self.assertValidJson(response.content)

    def test_inactive_user_token(self):
        user = create_user(
            password=self.user_password,
        )
        token = self.get_token(
            username=user.username,
            password=self.user_password,
        )
        user.is_active = False
        user.save()
        self.validate_token_against_api(token, 401)

    def test_token_expiry(self):
        expiring = datetime.now() + timedelta(seconds=1)
        token = self.get_token(expiring=expiring)
        self.validate_token_against_api(token)
        sleep(1.1)
        response, content = self.validate_token_against_api(token, 401)
        self.assertEqual(content['detail'], 'Expired token.')

    def test_user_token_in_db(self):
        """Especially testing that the token is linked to the specific user."""
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
        self.validate_token_against_api(None, 401)
        self.validate_token_against_api('invalid', 401)
        token = self.get_token()
        self.validate_token_against_api(token, 200)

    def test_token_new(self):
        token = self.get_token()
        response, content = self.api_call(
            '/api/authentication/token/',
            token=token,
            method='post',
            payload={
                'application': self.__class__.__name__,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in content)

        # Disabled until #79 is fixed
        #
        # token = self.get_token(renewable=False)
        # response, content = self.api_call(
        #     '/api/authentication/token/',
        #     token=token,
        #     method='post',
        #     payload={
        #         'application': self.__class__.__name__,
        #     }
        # )
        # self.assertEqual(response.status_code, 403)
        # self.assertFalse('token' in content)

    def test_token_delete(self):
        token = self.get_token()
        db_token = get_db_token(token)
        random_uuid = str(uuid.uuid4())
        response, content = self.api_call(
            f'/api/authentication/token/{random_uuid}/',
            token=token,
            method='delete',
        )
        self.assertEqual(response.status_code, 404)
        response, content = self.api_call(
            f'/api/authentication/token/{db_token.pk}/',
            token=token,
            method='delete',
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            get_db_token(token)
