import os
from datetime import datetime, timedelta

import jwt

secret = os.getenv("TOKEN_SECRET")


class JWT:
    @classmethod
    def create_token(cls, user_id):
        """ This function creates a new token
            after user login is successful.
         """
        utcnow = datetime.utcnow()
        # token signature
        user_data = {
            'user_id': user_id,
            'iat': utcnow,
            'exp': utcnow + timedelta(seconds=int(604800)),
        }
        # encode the token
        return jwt.encode(user_data,
                          secret,
                          algorithm='HS256').decode('utf-8')

    @classmethod
    def decode_token(cls, token):
        """ This function decodes the token and returns
            the user id if token is valid
        """
        try:
            user = jwt.decode(token, secret) # decode the token
            return user['user_id'] # return the user id used to sign token
        except jwt.exceptions.InvalidTokenError:
            # token is invalid, return error message
            return "Invalid Token, please login again"
