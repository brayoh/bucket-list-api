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

    def set_headers(self):
        """ Set headers for Authorization and Content Type. """
        self.client.post("/auth/register",
                         data=self.user,
                         content_type='application/json')

        response = self.client.post( "/auth/login",
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
