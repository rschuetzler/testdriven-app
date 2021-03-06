import json

from flask import current_app

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps(
                    {
                        "username": "justatest",
                        "email": "test@test.com",
                        "password": "123456",
                    }
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(data["message"] == "Successfully registered.")
            self.assertTrue(data["auth_token"])
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 201)

    def test_duplicate_user(self):
        add_user("test", "test@test.com", "123456")
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps(
                    {
                        "username": "test",
                        "email": "test@test2.com",
                        "password": "123456",
                    }
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn("Sorry. That user already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_duplicate_email(self):
        add_user("test2", "test@test.com", "123456")
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps(
                    {"username": "test", "email": "test@test.com", "password": "123456"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn("Sorry. That user already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                "/auth/register", data=json.dumps({}), content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json_no_username(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({"email": "test@test.com", "password": "test"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json_no_email(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({"username": "justatest", "password": "teset123"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_user_registration_invalid_json_no_password(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({"email": "test@test.com", "username": "justatest"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_registered_user_login(self):
        with self.client:
            add_user("test", "test@test.com", "test")
            response = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(data["message"] == "Successfully logged in.")
            self.assertTrue(data["auth_token"])
            self.assertTrue(response.content_type == "application/json")
            self.assert200(response)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "User does not exist.")
            self.assertTrue(response.content_type == "application/json")
            self.assert404(response)

    def test_valid_logout(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test"}),
                content_type="application/json",
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/logout", headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(data["message"] == "Successfully logged out.")
            self.assert200(response)

    def test_invalid_logout_expired_token(self):
        add_user("test", "test@test.com", "test")
        current_app.config["TOKEN_EXPIRATION_SECONDS"] = -1
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test"}),
                content_type="application/json",
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/logout", headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertTrue(
                data["message"] == "Signature expired. Please log in again."
            )
            self.assert401(response)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                "/auth/logout", headers={"Authorization": "Bearer invalid"}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "Invalid token. Please log in again.")
            self.assert401(response)

    def test_user_status(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com", "password": "test"}),
                content_type="application/json",
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/status", headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data["status"], "success")
            self.assertTrue(data["data"] is not None)
            self.assertEqual(data["data"]["username"], "test")
            self.assertEqual(data["data"]["email"], "test@test.com")
            self.assertTrue(data["data"]["active"] is True)
            self.assert200(response)

    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                "/auth/status", headers={"Authorization": "Bearer invalid"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid token. Please log in again.")
            self.assert401(response)

