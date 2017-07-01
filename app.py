from flask import Flask, request
from flask_restful import Api

from controllers.accounts_manager import AccountsManager
from controllers.bucketlist import BucketList

app = Flask(__name__)
api = Api(app)

api.add_resource(AccountsManager, '/auth/register', '/auth/login')
api.add_resource(BucketList,
                 '/bucketlists',
                 '/bucketlists/<id>')
api.add_resource(BucketListItems,
                 '/bucketlists/<id>/items',
                 '/bucketlists/<id>/items/<item_id>')


if __name__ == '__main__':
    app.run(debug=True)
