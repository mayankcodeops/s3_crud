import unittest
from app import create_app, db


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        """
        Creates context for a unit test case
        Initializes test app context and test database
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroys setUp context after a Unit Test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """Test response for root route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
