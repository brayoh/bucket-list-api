import logging
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, fields, marshal

from app.models import User, BucketList
from app.utils.db import save_record, delete_record
from app.utils.auth.authorize import login_required

logger = logging.getLogger(__name__)

# Field marshal for bucketlist item
bucketlist_fields = {"id": fields.Integer,
                     "name": fields.String,
                     "description": fields.String,
                     "created_at": fields.DateTime
                     }


class BucketListsResource(Resource):
    """ this class gets all the bucketlists in the database."""
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name",
                                 type=str,
                                 required=True,
                                 help="bucketlist name is required")

        self.parser.add_argument("description",
                                 type=str,
                                 required=True,
                                 help="bucketlist description is required")

    @login_required
    def get(self, user_id, response):
        return make_response(jsonify({
            "message": response[0]
        }), response[1])


class BucketListResource(Resource):
    """ this class gets a single bucketlist. """
    @login_required
    def get(self, id, user_id, response):
        if user_id is not None:
            user = User.query.filter_by(id=user_id)
            if user:
                logger.info("this is the user id %(user_id)")
            else:
                response = ("Please login to access your bucketlists", 401)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])
