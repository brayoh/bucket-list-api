import json
from base import Base


class TestItemResource(Base):
    """ This class contains tests for login and registeration
        of user accounts
    """

    def test_gets_single_item(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/bucketlists/1/items/1",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["name"], "go bunjee jumping")

        self.assertFalse(payload["done"])
        self.assertEquals(response.status_code, 200)

    def test_updates_item(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

        response = self.client.put("/bucketlists/1/items/1",
                                   data=json.dumps({
                                       "name": "go climbing",
                                       "done": True

                                   }),
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"], "Item updated successfully")
        self.assertEquals(response.status_code, 200)

    def test_update_item_with_same_name(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

        response = self.client.put("/bucketlists/1/items/1",
                                   data=json.dumps({
                                       "name": "go bunjee jumping",
                                   }),
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())

        self.assertEquals(payload["message"],
                          "Item with similar name already exists")
        self.assertEquals(response.status_code, 409)

    def test_get_non_existing_item(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/bucketlists/1/items",
                         data=json.dumps({
                             "name": "dare devil"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/bucketlists/1/items/2",
                                   headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Item not found")
        self.assertEquals(response.status_code, 404)


    def test_deletes_item(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())


        response = self.client.delete("/bucketlists/1/items/1",
                                     headers=self.set_headers())

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Item deleted successfully")

        self.assertEquals(response.status_code, 200)

    def test_get_method_is_protected(self):
        self.client.post("/bucketlists",
                         data=json.dumps({
                             "name": "dare devil",
                             "description": "testing"
                         }),
                         headers=self.set_headers())

        self.client.post("/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

        response = self.client.get("/bucketlists/1/items/1")

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

        self.client.post("/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())

        response = self.client.put("/bucketlists/1/items/1",
                                   data=json.dumps({
                                       "name": "go climbing"
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

        self.client.post("/bucketlists/1/items",
                         data=json.dumps({
                             "name": "go bunjee jumping"
                         }),
                         headers=self.set_headers())


        response = self.client.delete("/bucketlists/1/items/1")

        payload = json.loads(response.data.decode())
        self.assertEquals(payload["message"],
                          "Please login to access your bucketlists")
        self.assertEquals(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
