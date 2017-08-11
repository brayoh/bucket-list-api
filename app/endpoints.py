""" This file contains all the api endpoints. """
from flask import Blueprint
from flask_restful import Api

from app.controllers.accounts_manager import LoginResource, RegisterResource
from app.controllers.bucketlist import BucketListsResource, BucketListResource
from app.controllers.bucketlist_items import ItemsResource, ItemResource


bucketlist_blueprint = Blueprint('bucket_list', __name__)
api = Api(bucketlist_blueprint)

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
