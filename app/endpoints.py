from flask import request, Blueprint
from flask_restful import Api

from controllers.accounts_manager import AccountsManager
from controllers.bucketlist import BucketList
from controllers.bucketlist_items import BucketListItems


bucketlist_blueprint = Blueprint('bucket_list', __name__)
api = Api(bucketlist_blueprint)

api.add_resource(AccountsManager, '/auth/register', '/auth/login')
api.add_resource(BucketList,
                 '/bucketlists',
                 '/bucketlists/<int:id>')

api.add_resource(BucketListItems,
                 '/bucketlists/<int:bucketlist_id>/items',
                 '/bucketlists/<int:bucketlist_id>/items/<item_id>')
