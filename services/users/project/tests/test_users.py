import json
import unittest

# from project import db
# from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    """Tests for users service."""

    def test_users(self):
        """Ensure the /ping route behaves"""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added"""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"username": "ryan", "email": "ryan@example.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("ryan@example.com was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if JSON is empty"""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "ryan@example.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists"""
        with self.client:
            user = {"username": "ryan", "email": "ryan@example.com"}
            self.client.post(
                "/users", data=json.dumps(user), content_type="application/json"
            )
            response = self.client.post(
                "/users", data=json.dumps(user), content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("email already exists", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure getting a single user behaves correctly."""
        user = add_user("ryan", "ryan@example.com")
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assert200(response)
            self.assertIn("ryan", data["data"]["username"])
            self.assertIn("ryan@example.com", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Ensure error is thrown if ID is not provided."""
        with self.client:
            response = self.client.get("/users/blah")
            data = json.loads(response.data.decode())
            self.assert404(response)
            self.assertIn("No user ID provided", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assert404(response)
            self.assertIn("User does not exist", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        """Ensure get all users behaves correct."""
        add_user("ryan", "ryan@example.com")
        add_user("steve", "steve@example.com")
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assert200(response)
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertIn("ryan", data["data"]["users"][0]["username"])
            self.assertIn("steve", data["data"]["users"][1]["username"])
            self.assertIn("ryan@example.com", data["data"]["users"][0]["email"])
            self.assertIn("steve@example.com", data["data"]["users"][1]["email"])
            self.assertIn("success", data["status"])

    def test_main_no_users(self):
        """Ensure the main route works with no users in DB"""
        response = self.client.get("/")
        self.assert200(response)
        self.assertIn(b"<h1>All Users</h1>", response.data)
        self.assertIn(b"<p>No users!</p>", response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves when users are added"""
        add_user("ryan", "ryan@example.com")
        add_user("michael", "michael@example.net")
        with self.client:
            response = self.client.get("/")
            self.assert200(response)
            self.assertIn(b"<h1>All Users</h1>", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"ryan", response.data)
            self.assertIn(b"michael", response.data)

    def test_main_add_user(self):
        """Ensure we can add new users to the database"""
        with self.client:
            response = self.client.post(
                "/",
                data=dict(username="ryan", email="ryan@example.com"),
                follow_redirects=True,
            )
            self.assert200(response)
            self.assertIn(b"<h1>All Users</h1>", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"ryan", response.data)


if __name__ == "__main__":
    unittest.main()
