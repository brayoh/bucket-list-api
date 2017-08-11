import logging
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, fields, marshal

from app.models import BucketList, Item
from app.common.db import save_record, delete_record
from app.common.auth.authorize import login_required

logger = logging.getLogger(__name__)

# Field marshal for bucketlist item
bucketlist_item_fields = {"id": fields.Integer,
                         "name": fields.String,
                         "done": fields.Boolean,
                         "bucketlist_id": fields.Integer,
                         "created_at": fields.DateTime
                         }


class ItemsResource(Resource):
    """ This class handles CRUD actions for bucketlist items. """
    method_decorators = [login_required]  # applies to all inherited resources

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name",
                                 type=str,
                                 required=True,
                                 help="item name is required",
                                 location="json")

    def get(self, blist_id=None, user_id=None, response=None):
        if user_id and blist_id is not None:
            bucketlist = BucketList.query.filter_by(id=blist_id,
                                                    user_id=user_id).first()

            if bucketlist:
                items = Item.query.filter_by(bucketlist_id=blist_id).all()
                return marshal(items, bucketlist_item_fields), 200
            else:
                response = ("Bucketlist not found", 404)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])


    def post(self, blist_id=None, user_id=None, response=None):
        args = self.parser.parse_args()
        name = args["name"]

        if user_id and blist_id is not None:
            # get bucketlist from db using the primary key
            bucketlist = BucketList.query.filter_by(id=blist_id,
                                                    user_id=user_id).first()

            # check if bucketlist is owned by this user
            if bucketlist:
                if Item.query.filter_by(name=name).first():
                    response = ("Item with similar name already exists", 409)
                else:
                    item = Item(name, blist_id)
                    save_record(item)
                    response = ("Item created successfully", 201)
            else:
                response = ("Bucketlist not found", 404)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])


class ItemResource(Resource):
    """ This class handles CRUD actions for bucketlist items. """
    method_decorators = [login_required]  # applies to all inherited resources

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name",
                                 type=str,
                                 required=True,
                                 help="item name is required",
                                 location="json")
        self.parser.add_argument("done",
                                 type=bool,
                                 default=False,
                                 location="json")


    def get(self, blist_id=None, user_id=None, item_id=None, response=None):

        if all(param is not None for param in [blist_id, user_id, item_id]):
            # get bucketlist using the primary key
            bucketlist = BucketList.query.filter_by(id=blist_id,
                                                    user_id=user_id).first()

            # check if bucketlist is owned by this user
            if bucketlist:
                item = Item.query.get(item_id)
                if item:
                    return marshal(item, bucketlist_item_fields), 200
                else:
                    response = ("Item not found", 404)
            else:
                response = ("Bucketlist not found", 404)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])


    def put(self, blist_id=None, user_id=None, item_id=None, response=None):

        args = self.parser.parse_args()
        name = args["name"]
        done = args["done"]

        if user_id and id is not None:
            # get bucketlist from db using the primary key
            bucketlist = BucketList.query.filter_by(id=blist_id,
                                                    user_id=user_id).first()

            if bucketlist:
                if Item.query.filter_by(name=name).first():
                    response = ("Item with similar name already exists", 409)
                else:
                    item = Item.query.get(item_id)
                    item.name = name
                    item.done = done

                    save_record(item)
                    response = ("Item updated successfully", 200)
            else:
                response = ("Bucketlist not found", 404)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])


    def delete(self, blist_id=None, user_id=None, item_id=None, response=None):

        if user_id and blist_id is not None:
            bucketlist = BucketList.query.filter_by(id=blist_id,
                                                    user_id=user_id).first()
            if bucketlist:
                item = Item.query.get(item_id)
                if item:
                    delete_record(item)
                    response = ("Item deleted successfully", 200)
                else:
                    response = ("Item not found", 404)
            else:
                response = ("Bucketlist not found", 404)

        return make_response(jsonify({
            "message": response[0]
        }), response[1])
