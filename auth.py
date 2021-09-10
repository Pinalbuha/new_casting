import os
from functools import wraps
import json
from flask import request, _request_ctx_stack, abort
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

class AuthError(Exception):
    ''' Way to communicate with auth failures'''

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_from_auth_header():
    '''function will get access token from auth header'''
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        raise AuthError({
            'code': 'Missing Authorization Header',
            'description': 'Authorization header must be included'
        }, 401)

    # folding auth header parts
    auth_header_parts = auth_header.split()
    if len(auth_header_parts) == 1:
        raise AuthError({
            'code': 'header is invalid ,it should have 2 parts',
            'description': 'Token is not found'
        }, 401)

    # first part of the header should be Bearer
    elif auth_header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'Invalid header',
            'description': 'Header must be starts with Bearer'
        }, 401)

    # checking for more that 2 parts in auth header
    elif len(auth_header_parts) > 2:
        raise AuthError({
            'code': 'header is invalid',
            'description': 'Authorization Header must be Bearer token'
        }, 401)

    jwt_token = auth_header_parts[1]
    return jwt_token


'''
decode and verify jwt token to check whether it is valid or not.
'''
def verify_decode_jwt(jwt_token):
    # this will get public key from Auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(jwt_token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Authorization was malformed.'
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

    if rsa_key:
        try:
            payload = jwt.decode(
                jwt_token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token expired',
                'description': 'Token has expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid claims',
                'description': 'Incorrect claims. Please, check' + 'the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid header',
                'description': 'Unable to parse the authentication jwt token.'
            }, 401)
    raise AuthError({
        'code': 'invalid header',
                'description': 'Unable to find appropriate key.'
    }, 401)


'''
this function will check permission for given token
'''
def check_permissions(permission, payload):
    get_permission = payload.get('permissions')
    # permission not found
    if not get_permission:
        raise AuthError({'code': 'invalid_claims', 'description': 'Permissions were not included in the JWT token .'
                         }, 400)
    # requested permission not supported by JWT token
    if permission not in get_permission:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission denied.'
        }, 401)
    return True


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # get token
            token = get_token_from_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            # check permission
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
