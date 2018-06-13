import unittest
from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        """Ensure we can add a user."""

        user = add_user("justatest", "test@test.com", "superpass")
        self.assertTrue(user.id)
        self.assertEqual(user.username, "justatest")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        """Ensure we can't insert two users with same name."""
        add_user(
            username="justatest", email="test@test.com", password="supergoodpassword"
        )
        duplicate_user = User(
            username="justatest", email="test@test2.com", password="supergoodpassword"
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        """Ensure we can't add two users with same email."""
        add_user(
            username="justatest", email="test@test.com", password="supergoodpassword"
        )
        duplicate_user = User(
            username="justanothertest",
            email="test@test.com",
            password="supergoodpassword",
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user(
            username="justatest", email="test@test.com", password="uperdeeduperpass"
        )
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user("justatest", "test@test.com", "greatherthaneight")
        user_two = add_user("justatest2", "test@test2.com", "greatherthaneight")
        self.assertNotEqual(user_one.password, user_two.password)


if __name__ == "__main__":
    unittest.main()
