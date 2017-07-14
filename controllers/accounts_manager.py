from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app.models import User
from app.db_instance import save
from validator import validate

class LoginResource(Resource):
    """this class handles login and authentication"""
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username',
                            type=str,
                            required=True,
                            help="username is required")
        self.parser.add_argument('password',
                            type=str,
                            required=True,
                            help="password is required")

    def post(self):
        args = self.parser.parse_args(strict=True)
        username = args.get("username").strip()
        password = args.get("password").strip()

        if any(arg == "" for arg in [username, password]):
            message = "username and password is required"
            status = 400
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.verify_password(password):
                    message = "login successful"
                    status = 200
                else:
                    message = "username or password is incorrect"
                    status = 401
            else:
                message = "username or password is incorrect"
                status = 401

        return make_response(jsonify({
            "message": message
        }), status)


class RegisterResource(Resource):
    """docstring for AccountsManager."""
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username',
                            type=str,
                            required=True,
                            help="username is required")
        self.parser.add_argument('password',
                            type=str,
                            required=True,
                            help="password is required")

    def post(self):
        args = self.parser.parse_args(strict=True)
        username = args.get("username")
        password = args.get("password")

        if any(arg == "" for arg in [username, password]):
            message = "username and password is required"
            status = 400
        elif not username.isalpha():
            message = "username should not contain special characters"
            status = 400
        elif len(password) < 6:
            message = "password should be more than 6 characters"
            status = 400
        elif User.query.filter_by(username=username).first():
            message = "username already exists"
            status = 409
        else:
            user = User(username, password)
            save(user)

            message = "user registered successfully"
            status = 201


        return make_response(jsonify({
            "message": message
        }), status)
