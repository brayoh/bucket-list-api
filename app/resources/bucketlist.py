import logging
import pprint
from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse, fields, marshal

from app.models import BucketList
from app.common.db import save_record, delete_record
from app.common.auth.authorize import login_required

logger = logging.getLogger(__name__)

bucketlist_item_fields = {"id": fields.Integer,
                         "name": fields.String,
                         "done": fields.Boolean,
                         "bucketlist_id": fields.Integer,
                         "created_at": fields.DateTime,
                         "updated_at": fields.DateTime
                         }

# Field marshal for bucketlist item
bucketlist_fields = {"id": fields.Integer,
                     "name": fields.String,
                     "description": fields.String,
                     "created_at": fields.DateTime,
                     "updated_at": fields.DateTime,
                     "items": fields.List(fields.Nested(bucketlist_item_fields))
                     }

# Field marshal for bucketlist item


class BucketListsResource(Resource):
    """ This class handles creation and getting of bucketlists. """
    method_decorators = [login_required]  # applies to all inherited resources

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

    def get(self, user_id=None, response=None):
        """ This function handles get requests. """

        if user_id is not None:

            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument(
                'page', type=int, location='args',
                default=1
            )
            self.reqparse.add_argument(
                'limit',
                type=int,
                default=20,
                location='args'
            )
            self.reqparse.add_argument(
                'q', type=str,
                location='args'
            )
            args = self.reqparse.parse_args()

            q = args['q']
            page = args['page']
            limit = args['limit']

            # Pagination logic
            if q:
                bucketlist = BucketList.query.filter(
                                            BucketList.name.\
                                            ilike('%' + q + '%'),\
                                            BucketList.user_id==user_id)\
                                            .paginate(page, limit, False)
            else:
                bucketlist = BucketList.query.filter_by(user_id=user_id)\
                                            .paginate(page, limit, False)

            if bucketlist.has_next:
                url = request.url.split("?limit")[0]
                next_page = url + '?limit=' + \
                    str(limit) + '&page=' + str(page + 1)
            else:
                next_page = 'Null'

            if bucketlist.has_prev:
                url = request.url.split("?limit")[0]
                prev_page = url + '?limit=' + \
                    str(limit) + '&page=' + str(page - 1)
            else:
                prev_page = 'Null'

            return {'meta': {'next_page': next_page,
                             'prev_page': prev_page,
                             'total_pages': bucketlist.pages
                             },
                    'bucketlists': marshal(bucketlist.items, bucketlist_fields)
                    }, 200

        return make_response(jsonify({
            "status": response[0],
            "message": response[1]
        }), response[2])


    def post(self, user_id=None, response=None):
        """ This function handles post requests. """

        args = self.parser.parse_args()
        name = args["name"]
        description = args["description"]

        if user_id is not None:

            if BucketList.query.filter_by(user_id=user_id, name=name).first():
                response = ("failed",
                            "Bucketlist with a similar name exists", 409)
            else:
                bucketlist = BucketList(name, description, user_id)
                save_record(bucketlist)

                response = ("success", "Bucketlist created successfully", 201)

        return make_response(jsonify({
            "status": response[0],
            "message": response[1]
        }), response[2])


class BucketListResource(Resource):
    """ This class gets a single bucketlist. """
    method_decorators = [login_required]  # applies to all inherited resources

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

    def get(self, id=None, user_id=None, response=None):
        """ This function handles get requests. """

        if user_id and id is not None:
            bucketlist = BucketList.query.filter_by(id=id,
                                                    user_id=user_id).first()
            if bucketlist:
                return marshal(bucketlist, bucketlist_fields), 200
            else:
                response = ("failed","Bucketlist not found", 404)
        else:
            response = ("failed",
                        "Please login to access your bucketlists", 401)

        return make_response(jsonify({
            "status": response[0],
            "message": response[1]
        }), response[2])


    def put(self, id=None, user_id=None, response=None):
        """ This function handles put requests. """

        args = self.parser.parse_args()
        name = args["name"]
        description = args["description"]

        if user_id and id is not None:
            bucketlist = BucketList.query.filter_by(id=id,
                                                    user_id=user_id).first()
            if bucketlist:
                if BucketList.query.filter_by(user_id=user_id,
                                              name=name).first():
                    response = ("failed",
                                "Bucketlist with a similar name exists", 409)
                else:
                    bucketlist.name = name
                    bucketlist.description = description

                    # save the newly updated record
                    save_record(bucketlist)
                    response = ("success",
                                "bucketlist updated successfully", 200)
            else:
                response = ("failed", "Bucketlist not found", 404)
        else:
            response = ("failed",
                        "Please login to access your bucketlists", 401)

        return make_response(jsonify({
            "status": response[0],
            "message": response[1]
        }), response[2])


    def delete(self, id=None, user_id=None, response=None):
        """ This function handles delete requests. """

        if user_id and id is not None:
            bucketlist = BucketList.query.filter_by(id=id,
                                                    user_id=user_id).first()
            if bucketlist:
                delete_record(bucketlist)
                response = ("success", "Bucketlist deleted successfully", 200)
            else:
                response = ("failed", "Bucketlist not found", 404)
        else:
            response = ("failed",
                        "Please login to access your bucketlists", 401)

        return make_response(jsonify({
            "status": response[0],
            "message": response[1]
        }), response[2])
