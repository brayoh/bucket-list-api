import json
from tests.base import Base


class TestAccountsManagerResource(Base):
    """ This class contains tests for login and registeration
        of user accounts
    """
    def test_register_user(self):
        payload = self.client.post("/api/v1/auth/register",
                                   data=self.user,
                                   content_type='application/json')

        reponse = json.loads(payload.data.decode())

        self.assertEquals(reponse['message'],
                          "user registered successfully")
        self.assertEquals(payload.status_code, 201)

    def test_logins_user(self):
        self.client.post("/api/v1/auth/register",
                         data=self.user,
                         content_type='application/json')

        payload = self.client.post("/api/v1/auth/login",
                                   data=self.user,
                                   content_type='application/json')

        reponse = json.loads(payload.data.decode())
        self.assertIn("token", reponse, "response should contain token")
        self.assertEquals(payload.status_code, 200)
        
    # tests for /api/v1/auth/login
    def test_wrong_credentials(self):
        self.client.post("/api/v1/auth/register",
                         data=self.user,
                         content_type='application/json')

        payload = self.client.post("/api/v1/auth/login",
                                   data=json.dumps({
                                       "username": "brian",
                                       "password": "pass"
                                   }),
                                   content_type='application/json')
        reponse = json.loads(payload.data.decode())

        self.assertEquals(reponse['message'],
                          "username or password is incorrect")
        self.assertEquals(payload.status_code, 401)

    def test_empty_login_not_allowed(self):
        payload = self.client.post("/api/v1/auth/login",
                                   data=json.dumps({
                                       "username": "",
                                       "password": ""
                                   }),
                                   content_type='application/json')

        reponse = json.loads(payload.data.decode())
        self.assertEquals(reponse['message'],
                          "username and password is required")
        self.assertEquals(payload.status_code, 400)

    # tests for /api/v1/auth/register
    def test_duplicate_username(self):
        self.client.post("/api/v1/auth/register",
                         data=self.user,
                         content_type='application/json')

        payload = self.client.post("/api/v1/auth/register",
                                   data=self.user,
                                   content_type='application/json')
        reponse = json.loads(payload.data.decode())

        self.assertEquals(reponse['message'],
                          "username already exists")
        self.assertEquals(payload.status_code, 409)

    def test_non_registered_user(self):
        payload = self.client.post("/api/v1/auth/login",
                                   data=self.user,
                                   content_type='application/json')

        reponse = json.loads(payload.data.decode())

        self.assertEquals(reponse['message'],
                          "username or password is incorrect")
        self.assertEquals(payload.status_code, 401)

    def test_special_characters_denied(self):
        payload = self.client.post("/api/v1/auth/register",
                                   data=json.dumps({
                                       "username": "brian445##$#$",
                                       "password": "password"
                                   }),
                                   content_type='application/json')

        reponse = json.loads(payload.data.decode())
        self.assertEquals(reponse['message'],
                          "username should not contain special characters")
        self.assertEquals(payload.status_code, 400)

    def test_empty_inputs_not_allowed(self):
        payload = self.client.post("/api/v1/auth/register",
                                   data=json.dumps({
                                       "username": "",
                                       "password": ""
                                   }),
                                   content_type='application/json')

        reponse = json.loads(payload.data.decode())
        self.assertEquals(reponse['message'],
                          "username and password is required")
        self.assertEquals(payload.status_code, 400)

    def test_password_length(self):
        payload = self.client.post("/api/v1/auth/register",
                                   data=json.dumps({
                                       "username": "brian",
                                       "password": "pass"
                                   }),
                                   content_type='application/json')

        reponse = json.loads(payload.data.decode())
        self.assertEquals(reponse['message'],
                          "password should be more than 6 characters")
        self.assertEquals(payload.status_code, 400)


if __name__ == "__main__":
    unittest.main()
