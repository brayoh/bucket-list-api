import json
from tests.base import Base


class TestBucketlistsResource(Base):
    """ This class contains tests for BucketListsResource
    """
    def test_creates_bucketlist(self):
        response = self.client.post("/api/v1/bucketlists",
                                     data=json.dumps({
                                         "name": "dare devil 2",
                                         "description": "testing"
                                     }),
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Bucketlist created successfully")
        self.assertEquals(response.status_code, 201)

    def test_duplicate_bucketlist(self):

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
                                         "name": "dare devil 3",
                                         "description": "testing"
                                     }),
                                     content_type="application/json")


        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Please login to access your bucketlists")
        self.assertEquals(response.status_code, 401)

    def test_search_bucketlist(self):
        response = self.client.get("/api/v1/bucketlists?q=dare",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["bucketlists"][0]["name"],
                          "dare devil")
        self.assertEquals(response.status_code, 200)

    def test_pagination_has_next(self):

        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "testing one",
                             "description": "testing 1"
                         }),
                         headers=self.set_headers())

        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "another one",
                             "description": "another"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/api/v1/bucketlists?limit=2&page=1",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["meta"]["next_page"],
                          "http://localhost/api/v1/bucketlists?limit=2&page=2")
        self.assertEquals(len(payload["bucketlists"]), 2)
        self.assertEquals(response.status_code, 200)

    def test_pagination_has_previous(self):

        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "testing one",
                             "description": "testing 1"
                         }),
                         headers=self.set_headers())

        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "another one",
                             "description": "another"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/api/v1/bucketlists?limit=1&page=2",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["meta"]["prev_page"],
                          "http://localhost/api/v1/bucketlists?limit=1&page=1")
        self.assertEquals(len(payload["bucketlists"]), 1)
        self.assertEquals(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
