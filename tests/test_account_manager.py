from base import Base


class TestAuthentication(Base):
    def test_register_user(self):
        payload = self.client.post("/auth/register", data=self.user)

        self.assertEquals(payload.status_code, 201)

    def test_duplicate_username(self):
        self.client.post("/auth/register", data=self.user)
        payload = self.client.post("/auth/register", data=self.user)

        self.assertEquals(payload.status_code, 409)

    def test_non_registered_user(self):
        payload = self.client.post("/auth/login", data=self.user)

        self.assertEquals(payload.status_code, 401)

    def test_wrong_credentials(self):
        self.client.post("/auth/register", data=self.user)
        self.user['password'] = "passwad"
        payload = self.client.post("/auth/login", data=self.user)

        self.assertEquals(payload.status_code, 401)

    def test_login(self):
        self.client.post("/auth/register", data=self.user)
        payload = self.client.post("/auth/login", data=self.user)

        self.assertEquals(payload.status_code, 200)


if __name__ == "__main__":
    unittest.main()
