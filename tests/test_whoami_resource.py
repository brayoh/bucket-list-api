import unittest
import json

from tests.base import Base


class TestWhoAmIResource(Base):
    """ This class tests the whoami resources by making a get request
        to /whoami with token set in the header
    """
    def test_returns_user_info(self):
        """ Get user info by making a request with a valid token """
        payload = self.client.get("/api/v1/whoami", headers=self.set_headers())
        reponse = json.loads(payload.data.decode())

        self.assertEquals(reponse["id"], 1)
        self.assertEquals(reponse["username"],"brian")
        self.assertEquals(payload.status_code, 200)

    def test_invalid_token_denied(self):
        """ Test if invalid token is allowed """
        payload = self.client.get("/api/v1/whoami", headers=
                                  dict({"Authorization": "tiainsansindad"}))
        reponse = json.loads(payload.data.decode())

        self.assertEquals(reponse["status"], "failed")
        self.assertEquals(reponse["message"],
                          "Invalid token, please login again")
        self.assertEquals(payload.status_code, 401)
