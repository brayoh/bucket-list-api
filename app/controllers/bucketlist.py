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
                                 help="bucketlist name is required",
                                 location="json")

        self.parser.add_argument("description",
                                 type=str,
                                 required=True,
                                 help="bucketlist description is required",
                                 location="json")

    @login_required
    def get(self, user_id=None, response=None):

        if user_id is not None:
            user_bucketlists = BucketList.query.filter_by(user_id=user_id).all()

            return marshal(user_bucketlists, bucketlist_fields), 200

        return make_response(jsonify({
            "message": response[0]
        }), response[1])


    @login_required
    def post(self, user_id=None, response=None):
        args = self.parser.parse_args()
        name = args["name"]
        description = args["description"]

        if user_id is not None:

            if BucketList.query.filter_by(name=name).first():
                response = ("Bucketlist with a similar name exists", 409)
            else:
                bucketlist = BucketList(name, description, user_id)
                data = save_record(bucketlist)

                response = ("Bucketlist created successfully", 201)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])


class BucketListResource(Resource):
    """ this class gets a single bucketlist. """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name",
                                 type=str,
                                 required=True,
                                 help="bucketlist name is required",
                                 location="json")

        self.parser.add_argument("description",
                                 type=str,
                                 required=True,
                                 help="bucketlist description is required",
                                 location="json")

    @login_required
    def get(self, id=None, user_id=None, response=None):
        if user_id and id is not None:
            bucketlist = BucketList.query.filter_by(id=id,
                                                    user_id=user_id).first()
            if bucketlist:
                return marshal(bucketlist, bucketlist_fields), 200
            else:
                response = ("Bucketlist not found", 404)
        else:
            response = ("Please login to access your bucketlists", 401)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])


    @login_required
    def put(self, id=None, user_id=None, response=None):
        args = self.parser.parse_args()
        name = args["name"]
        description = args["description"]

        if user_id and id is not None:
            bucketlist = BucketList.query.filter(id=id,
                                                 user_id=user_id).first()
            if bucketlist:
                if BucketList.query.filter_by(name=name).first():
                    response = ("Bucketlist with a similar name exists", 409)
                else:
                    bucketlist.name = name
                    bucketlist.description = description

                    # save the newly updated record
                    save_record(bucketlist)
                    response = ("bucketlist updated successfully", 200)
            else:
                response = ("Bucketlist not found", 404)
        else:
            response = ("Please login to access your bucketlists", 401)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])


    @login_required
    def delete(self, id=None, user_id=None, response=None):
        if user_id and id is not None:
            bucketlist = BucketList.query.filter_by(id=id,
                                                    user_id=user_id).first()
            if bucketlist:
                delete_record(bucketlist)
                response = ("Bucketlist deleted successfully", 200)
            else:
                response = ("Bucketlist not found", 404)
        else:
            response = ("Please login to access your bucketlists", 401)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])
