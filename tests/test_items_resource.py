import json
from tests.base import Base


class TestItemsResource(Base):
    """ This class contains tests for login and registeration
        of user accounts
    """

    def test_creates_new_item(self):
        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.post("/api/v1/bucketlists/1/items",
                                     data=json.dumps({
                                         "name": "go bunjee jumping"
                                     }),
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())

        self.assertEquals(payload["message"], "Item created successfully")
        self.assertEquals(response.status_code, 201)

    def test_gets_all_items(self):
        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/api/v1/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

        self.client.post("/api/v1/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go climbing"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/api/v1/bucketlists/1/items",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())

        self.assertEquals(len(payload), 2)
        self.assertEquals(response.status_code, 200)


    def test_get_non_existing_bucket_items(self):
        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/api/v1/bucketlists/1/items",
                         data=json.dumps({
                             "name": "dare devil"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/api/v1/bucketlists/2/items",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Bucketlist not found")
        self.assertEquals(response.status_code, 404)

    def test_create_item_with_same_name(self):
        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/api/v1/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

        response = self.client.post("/api/v1/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

        payload = json.loads(response.data.decode())

        self.assertEquals(payload["message"],
                          "Item with similar name already exists")
        self.assertEquals(response.status_code, 409)

    def test_no_items_4_missing_bucket(self):
        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        response = self.client.post("/api/v1/bucketlists/2/items",
                                     data=json.dumps({
                                         "name": "dare devil"
                                     }),
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Bucketlist not found")
        self.assertEquals(response.status_code, 404)


    def test_get_method_is_protected(self):
        self.client.post("/api/v1/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/api/v1/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/api/v1/bucketlists/1/items")

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Please login to access your bucketlists")
        self.assertEquals(response.status_code, 401)



if __name__ == "__main__":
    unittest.main()
