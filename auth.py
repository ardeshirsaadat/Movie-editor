import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = [os.environ['ALGORITHMS']]
API_AUDIENCE = os.environ['API_AUDIENCE']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError(
            {
                'code': 'invalid header',
                'description': 'Authorization header is not present'
            }, 401)

    auth_header = request.headers['Authorization']
    auth_header_array = auth_header.split(' ')

    if len(auth_header_array) != 2:
        raise AuthError(
            {
                'code': 'invalid header',
                'description': 'Authorization headers length not correct'
            }, 401)

    if auth_header_array[0].lower() != 'bearer':
        raise AuthError(
            {
                'code': 'invalid header',
                'description': 'Authorization header is missing bearer'
            }, 401)

    return auth_header_array[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError(
            {
                'code': 'invalid permission',
                'description': 'permissions  not present in payload'
            }, 401)

    if permission not in payload['permissions']:
        raise AuthError(
            {
                'code': 'invalid permission',
                'description': 'permissions do not match'
            }, 401)

    return True


def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(token,
                                 rsa_key,
                                 algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer='https://' + AUTH0_DOMAIN + '/')

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    'code':
                    'invalid_claims',
                    'description':
                    'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
        except Exception:
            raise AuthError(
                {
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
    raise AuthError(
        {
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
