import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        """
        Creates context for a unit test case
        Initializes test app context and test database
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Destroys setUp context after a Unit Test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """Test for existence of test app context"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """Test for asserting application configuration"""
        self.assertTrue(current_app.config['TESTING'])
