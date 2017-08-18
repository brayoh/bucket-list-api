import json
from tests.base import Base


class TestBucketlistsResource(Base):
    """ This class contains tests for BucketListsResource
    """
    def test_creates_bucketlist(self):
        response = self.client.post("/api/v1/bucketlists",
                                     data=json.dumps({
                                         "name": "dare devil",
                                         "description": "testing"
                                     }),
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Bucketlist created successfully")
        self.assertEquals(response.status_code, 201)

    def test_duplicate_bucketlist(self):
        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.post("/api/v1/bucketlists",
                                     data=json.dumps({
                                         "name": "dare devil",
                                         "description": "testing"
                                     }),
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Bucketlist with a similar name exists")
        self.assertEquals(response.status_code, 409)

    def test_gets_all_bucketlists(self):
        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/api/v1/bucketlists",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(len(payload["bucketlists"]), 1)
        self.assertEquals(response.status_code, 200)

    def test_get_method_is_protected(self):
        # make a request with no token set
        response = self.client.get("/api/v1/bucketlists")

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Please login to access your bucketlists")
        self.assertEquals(response.status_code, 401)

    def test_post_method_is_protected(self):
        # make a request with no token set
        response = self.client.post("/api/v1/bucketlists",
                                     data=json.dumps({
                                         "name": "dare devil",
                                         "description": "testing"
                                     }),
                                     content_type="application/json")


        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Please login to access your bucketlists")
        self.assertEquals(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
