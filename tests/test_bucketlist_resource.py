import json
from base import Base


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

if __name__ == "__main__":
    unittest.main()
