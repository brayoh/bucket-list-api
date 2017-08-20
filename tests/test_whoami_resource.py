import unittest
import json

from tests.base import Base


class TestWhoAmIResource(Base):
    def test_returns_user_info(self):
        self.client.post("/api/v1/auth/register",
                         data=self.user,
                         content_type='application/json')
        payload = self.client.get("/api/v1/whoami", headers=self.set_headers())
        reponse = json.loads(payload.data.decode())

        self.assertEquals(reponse["id"], 1)
        self.assertEquals(reponse["username"],"brian")
        self.assertEquals(payload.status_code, 200)

    def test_invalid_token_denied(self):
        self.client.post("/api/v1/auth/register",
                         data=self.user,
                         content_type='application/json')
        payload = self.client.get("/api/v1/whoami", headers=
                                  dict({"Authorization": "tiainsansindad"}))
        reponse = json.loads(payload.data.decode())

        self.assertEquals(reponse["status"], "failed")
        self.assertEquals(reponse["message"],
                          "Invalid token, please login again")
        self.assertEquals(payload.status_code, 401)
