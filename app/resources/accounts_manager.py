import logging
from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app.models import User
from app.common.db import save_record
from app.common.auth.token import JWT

logger = logging.getLogger(__name__)


class LoginResource(Resource):
    """ This class handles authentication of users. """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username",
                                 type=str,
                                 required=True,
                                 help="username is required",
                                 location="json")

        self.parser.add_argument("password",
                                 type=str,
                                 required=True,
                                 help="password is required",
                                 location="json")

    def post(self):
        """ This function handles post requests. """

        args = self.parser.parse_args()
        username = args.get("username").strip()
        password = args.get("password").strip()

        if any(arg == "" for arg in [username, password]):
            response = ("failed", "username and password is required", 400)
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.verify_password(password):
                    token = JWT.create_token(user.id)
                    return make_response(jsonify({
                        "status": "success",
                        "message": "login successful",
                        "token": token
                    }), 200)
                else:
                    response = ("failed",
                                "username or password is incorrect", 401)
            else:
                response = ("failed",
                            "username or password is incorrect", 401)

        return make_response(jsonify({
            "status": response[0],
            "message": response[1],
        }), response[2])


class RegisterResource(Resource):
    """ This class handles registration of users. """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username",
                                 type=str,
                                 required=True,
                                 help="username is required",
                                 location="json")

        self.parser.add_argument("password",
                                 type=str,
                                 required=True,
                                 help="password is required",
                                 location="json")

    def post(self):
        """ This function handles post requests. """

        args = self.parser.parse_args()
        username = args.get("username").strip()
        password = args.get("password").strip()

        if any(arg == "" for arg in [username, password]):
            response = ("username and password is required", 400)

        elif not username.isalpha():
            response = ("username should not contain special characters", 400)

        elif len(password) < 6:
            response = ("password should be more than 6 characters", 400)

        elif User.query.filter_by(username=username).first():
            response = ("username already exists", 409)

        else:
            user = User(username, password)

            # save the user data to the database
            save_record(user)

            response = ("user registered successfully", 201)

        # response is a tuple contain the response message and status code
        return make_response(jsonify({
            "message": response[0]
        }), response[1])
