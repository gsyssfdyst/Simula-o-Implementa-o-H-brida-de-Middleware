# common/auth.py
import time
import jwt
import config

class TokenManager:
    """Manage simple JWT creation and verification for node authentication.

    create_jwt(payload, exp_seconds=None):
        - Builds a JWT by attaching an expiration timestamp to the payload.
        - Uses SECRET_KEY from config to sign the token.
        - Explains that the payload should include node-identifying info.

    verify_jwt(token):
        - Verifies token signature and expiration.
        - Returns the decoded payload on success or raises jwt exceptions on failure.
    """

    def __init__(self, secret=None):
        self.secret = secret or config.SECRET_KEY

    def create_jwt(self, payload, exp_seconds=None):
        # Attach expiration to the payload so receivers can check token freshness.
        exp = int(time.time()) + (exp_seconds if exp_seconds is not None else config.TOKEN_EXPIRATION_SECONDS)
        data = payload.copy()
        data['exp'] = exp
        # Sign the token and return it. Consumers must verify signature and exp.
        token = jwt.encode(data, self.secret, algorithm='HS256')
        return token

    def verify_jwt(self, token):
        # Verify signature and expiration; jwt.decode will raise on invalid/expired tokens.
        decoded = jwt.decode(token, self.secret, algorithms=['HS256'])
        # Additional payload checks (issuer, audience) can be added here.
        return decoded