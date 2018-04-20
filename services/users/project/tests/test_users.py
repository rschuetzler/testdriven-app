import json
import unittest

from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Tests for users service."""

    def test_users(self):
        """Ensure the /ping route behaves"""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'ryan',
                    'email': 'ryan@example.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('ryan@example.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if JSON is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'ryan@example.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'ryan',
                    'email': 'ryan@example.com'
                }),
                content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('email already exists', data['message'])
            self.assertIn('fail', data['status'])


if __name__ == '__main__':
    unittest.main()
