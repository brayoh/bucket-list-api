import json
from tests.base import Base


class TestBucketlistResource(Base):
    """ This class contains tests for login and registeration
        of user accounts
    """

    def test_gets_single_bucketlist(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/bucketlists/1",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["name"], "dare devil")

        self.assertEquals(payload["description"], "testing")
        self.assertEquals(response.status_code, 200)

    def test_updates_bucketlist(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.put("/bucketlists/1",
                                     data=json.dumps({
                                         "name": "new title",
                                         "description": "description"
                                     }),
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "bucketlist updated successfully")

        self.assertEquals(response.status_code, 200)

    def test_deletes_bucketlist(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.delete("/bucketlists/1",
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Bucketlist deleted successfully")

        self.assertEquals(response.status_code, 200)

    def test_update_non_existing_bucket(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.put("/bucketlists/2",
                                     data=json.dumps({
                                         "name": "new title",
                                         "description": "description"
                                     }),
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Bucketlist not found")

        self.assertEquals(response.status_code, 404)

    def test_update_with_same_name(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.put("/bucketlists/1",
                                     data=json.dumps({
                                         "name": "dare devil",
                                         "description": "testing"
                                     }),
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Bucketlist with a similar name exists")

        self.assertEquals(response.status_code, 409)

    def test_get_non_existing_bucket(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/bucketlists/2",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())

        self.assertEquals(payload["message"],
                          "Bucketlist not found")
        self.assertEquals(response.status_code, 404)

    def test_delete_non_existing_bucket(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.delete("/bucketlists/2",
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Bucketlist not found")

        self.assertEquals(response.status_code, 404)


    def test_get_method_is_protected(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        # make a request with no token set
        response = self.client.get("/bucketlists/1")

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Please login to access your bucketlists")
        self.assertEquals(response.status_code, 401)

    def test_put_method_is_protected(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())
        # make a request with no token set
        response = self.client.put("/bucketlists/1",
                                     data=json.dumps({
                                         "name": "new title",
                                         "description": "description"
                                     }),
                                     content_type="application/json")


        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Please login to access your bucketlists")
        self.assertEquals(response.status_code, 401)

    def test_delete_method_is_protected(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())
        # make a request with no token set
        response = self.client.delete("/bucketlists/1")

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Please login to access your bucketlists")
        self.assertEquals(response.status_code, 401)

    def test_expired_token_not_allowed(self):
        # expired token
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
            eyJpYXQiOjE1MDA1Mzk3NjYsInVzZXJfaWQiOjYsImV4cCI6MTUwMDU3NTc2Nn0.\
            WWGVh96IcxWk8ObA9OrDYsgQAmkgc7-a5uTUEGEpsjk"

        response = self.client.post("/bucketlists",
                                     data=json.dumps({
                                         "name": "dare devil",
                                         "description": "testing"
                                     }),
                                     headers={
                                        "Authorization": token,
                                        "Content-Type": "application/json"
                                     })

        # decode the response json
        payload = json.loads(response.data.decode())
        # check if response message is as expected
        self.assertEquals(payload["message"],
                          "Invalid Token, please login again")
        self.assertEquals(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
