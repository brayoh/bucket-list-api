from flask import request, Blueprint
from flask_restful import Api

from controllers.accounts_manager import LoginResource, RegisterResource
from controllers.bucketlist import GetAllBucketLists, GetBucketList
from controllers.bucketlist_items import BucketListItems


bucketlist_blueprint = Blueprint('bucket_list', __name__)
api = Api(bucketlist_blueprint)

# login routes
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')

# bucketlist routes
api.add_resource(GetAllBucketLists, '/bucketlists')
api.add_resource(GetBucketList, '/bucketlists/<int:id>')

# bucketlist items routes
api.add_resource(BucketListItems,
                 '/bucketlists/<int:bucketlist_id>/items',
                 '/bucketlists/<int:bucketlist_id>/items/<int:item_id>')
