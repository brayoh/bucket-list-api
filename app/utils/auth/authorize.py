""" This is a decorator function to check if user is authorized
    to access a specific endpoint in the app
"""
import logging
from functools import wraps
from flask_restful import request

from app.models import User
from app.utils.auth.token import JWT

logger = logging.getLogger(__name__)


def login_required(func):
    """ Decorator logic """
    @wraps(func)
    def decorated(*args, **kwargs):
        """ This function gets the token from the request header
            and decodes it to see if the token is valid then gets the user
            with the user id which the token is signed with.
        """
        user_id = None
        try:
            token = request.headers['Authorization']
            user_id = JWT.decode_token(token)  # decode the token

            if isinstance(user_id, int):
                user = User.query.get(user_id)  # get user from token signature

                if user:
                    response = ("login was successful", 200)
                else:
                    response = ("Invalid token, please login again", 401)
            else:
                response = (user_id, 401)
                user_id = None

        except KeyError as err:
            response = ("Please login to access your bucketlists", 401)
            logger.error(err)  # log the error

        updated_kwargs = {
            "response": response,
            "user_id": user_id
        }

        # append updated_kwargs with the existing kwargs values
        for key, value in kwargs.items():
            updated_kwargs[key] = value

        return func(*args, **updated_kwargs)
    return decorated
