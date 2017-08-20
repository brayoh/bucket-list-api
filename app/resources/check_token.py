from flask import  make_response, jsonify
from flask_restful import Resource, reqparse, marshal, fields
from app.models import User
from app.common.auth.token import JWT

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "created_at": fields.DateTime
}

class WhoAmIResource(Resource):
    """ This class takes a token from the Authorization header
        and then returns the user info for the token if its valid
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Authorization",
                                 location="headers",
                                 required=True)

    def get(self):
        """ get method """
        args = self.parser.parse_args()
        token = args["Authorization"]  # get token from header

        try:
            user_id = int(JWT.decode_token(token))
            user = User.query.get(user_id)

            return marshal(user, user_fields), 200

        except ValueError:
            return make_response(jsonify({
                "status": "failed",
                "message": "Invalid token, please login again"
            }), 401)
