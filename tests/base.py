import unittest
import json
from app import create_app, db
from app.models import User


class Base(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.user = json.dumps({
            "username": "brian",
            "password": "password"
        })

        with self.app.app_context():
            db.create_all()
        # register new user
        self.client.post("/api/v1/auth/register",
                                   data=self.user,
                                   content_type='application/json')
        # add new bucketlist
        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())
        
        # add a new item
        self.client.post("/api/v1/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

    def set_headers(self):
        """ Set headers for Authorization and Content Type. """
        self.client.post("/api/v1/auth/register",
                         data=self.user,
                         content_type='application/json')

        response = self.client.post("/api/v1/auth/login",
                                   data=self.user,
                                   content_type='application/json')

        payload = json.loads(response.data.decode())

        # get the token from the reponse body
        self.token = payload['token']

        return dict({
                'Authorization': self.token,
                'Content-Type': 'application/json',
               })

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
