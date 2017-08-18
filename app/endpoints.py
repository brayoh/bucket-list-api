""" This file contains all the api endpoints. """
from flask import Blueprint
from flask_restful import Api

from app.resources.accounts_manager import LoginResource, RegisterResource
from app.resources.bucketlist import BucketListsResource, BucketListResource
from app.resources.bucketlist_items import ItemsResource, ItemResource


bucketlist_blueprint = Blueprint("bucketlist_api", __name__)
api = Api(bucketlist_blueprint, "/api/v1")

# login routes
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')

# bucketlist routes
api.add_resource(BucketListsResource, '/bucketlists')
api.add_resource(BucketListResource, '/bucketlists/<int:id>')

# bucketlist items routes
api.add_resource(ItemsResource,
                 '/bucketlists/<int:blist_id>/items',
                 '/bucketlists/<int:blist_id>/items/')

api.add_resource(ItemResource,
                 '/bucketlists/<int:blist_id>/items/<int:item_id>',
                 '/bucketlists/<int:blist_id>/items/<int:item_id>/')
