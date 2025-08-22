# common/auth.py
import jwt
import datetime
from config import SECRET_KEY, TOKEN_EXPIRATION_SECONDS

class AuthService:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.expiration = TOKEN_EXPIRATION_SECONDS

    def generate_token(self, node_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.expiration),
            'iat': datetime.datetime.utcnow(),
            'sub': node_id
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {'valid': True, 'node_id': payload['sub']}
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token expirado'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Token inválido'}