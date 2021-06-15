import json


class ApiTestMixin:
    def assertValidJson(self, content: str):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            self.fail('Failed to parse JSON')

    def api_call(self, path: str, payload: dict = None, token: str = None,
                 method: str = 'get', decode_json: bool = True):

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
        elif method == 'delete':
            response = self.client.delete(
                path,
                payload,
                **headers,
            )
        else:
            raise ValueError('method must be either get, post or delete')

        if decode_json:
            self.assertValidJson(response.content)
            return response, json.loads(response.content)
        else:
            return response, response.content
