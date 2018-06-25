import json

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
            self.assertTrue(data["message"] == "Successfully registered")
            self.assertTrue(data["auth_token"])
            self.assertTrue(response.content_type == "application/json")
            self.assert200(response)

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
            self.assertIn('fail', data['status'])

    def test_duplicate_email(self):
        add_user("test2", "test@test.com", "123456")
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps(
                    {
                        "username": "test",
                        "email": "test@test.com",
                        "password": "123456",
                    }
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn("Sorry. That user already exists.", data["message"])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
    def test_user_registration_invalid_json_no_username(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_no_email(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'justatest',
                    'password': 'teset123'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_no_password(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'test@test.com',
                    'username': 'justatest',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assert400(response)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
