import unittest
from fixtures.artifact import artifact_fixture
from fixtures.artifact import form_dict
from fixtures.artifact import updated_dict
from fixtures.artifact import duplicate_dict
from fixtures.artifact import artifact_fixture1

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from app import create_app, db
from app.models import Artifact


class FlaskClientTestCase(unittest.TestCase):
    """Test Client for Artifact Model"""
    def setUp(self):
        """
        Initialized test context for each test case, creates application context, test database
        and imports fixtures.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.artifact_fixture = artifact_fixture
        self.form = form_dict
        self.updated_dict = updated_dict
        self.duplicate_dict = duplicate_dict
        self.artifact_fixture1 = artifact_fixture1

    def tearDown(self):
        """Destroys setUp context"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_artifact_creation(self):
        """Test for artifact object creation from model in database"""
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.artifact_fixture[0]).first_or_404())

    def test_artifact_creation_when_obj_is_present(self):
        """Test for asserting IntegrityError on duplication object creation"""
        obj = Artifact(self.artifact_fixture)
        obj1 = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.add(obj1)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_artifact_updation(self):
        """Test for artifact update method"""
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact
                             .query.filter_by(objectID=self.artifact_fixture[0])
                             .first_or_404()
                             )
        art = Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404()
        art.isHighlight = True
        db.session.add(art)
        db.session.commit()
        self.assertEqual(bool(Artifact.query
                              .filter_by(objectID=self.artifact_fixture[0])
                              .first_or_404().isHighlight),
                         True)

    def test_artifact_updation_duplicate_obj_id(self):
        """Test assertion of IntegrityError for object update against existing objects"""
        obj = Artifact(self.artifact_fixture)
        obj1 = Artifact(self.artifact_fixture1)
        db.session.add(obj)
        db.session.add(obj1)
        db.session.commit()
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.artifact_fixture[0])
                             .first_or_404()
                             )
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.artifact_fixture1[0])
                             .first_or_404()
                             )
        artifact1 = Artifact.query.filter_by(objectID=self.artifact_fixture1[0]).first_or_404()
        artifact1.objectID = artifact_fixture[0]
        db.session.add(artifact1)

        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_artifact_deletion(self):
        """Test for artifact deletion"""
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.artifact_fixture[0])
                             .first_or_404()
                             )
        db.session.delete(Artifact.query
                          .filter_by(objectID=self.artifact_fixture[0])
                          .first()
                          )
        db.session.commit()
        self.assertIsNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first())

    def test_delete_non_existent(self):
        """Test for asserting UnmappedInstanceError for deleting non-existent object"""
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.artifact_fixture[0])
                             .first_or_404()
                             )
        db.session.delete(Artifact.query
                          .filter_by(objectID=self.artifact_fixture[0])
                          .first())
        db.session.commit()
        with self.assertRaises(UnmappedInstanceError):
            db.session.delete(Artifact.query
                              .filter_by(objectID=self.artifact_fixture[0])
                              .first()
                              )

    def test_create_route(self):
        """Test for 'new' route view"""
        response = self.client.post('/new', data=self.form)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.form['objectID'])
                             .first()
                             )

    def test_delete_route(self):
        """Test for 'delete' route view"""
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.artifact_fixture[0])
                             .first_or_404()
                             )
        response = self.client.get(f'/delete/{self.artifact_fixture[0]}')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Artifact.query
                          .filter_by(objectID=self.artifact_fixture[0])
                          .first()
                          )

    def test_delete_route_non_existent_data(self):
        """Test delete route for non existent artifact object deletion"""
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.artifact_fixture[0])
                             .first_or_404()
                             )
        db.session.delete(Artifact.query
                          .filter_by(objectID=self.artifact_fixture[0])
                          .first())
        db.session.commit()
        self.assertIsNone(Artifact.query
                          .filter_by(objectID=self.artifact_fixture[0])
                          .first()
                          )
        with self.assertRaises(UnmappedInstanceError):
            self.client.get(f'/delete/{self.artifact_fixture[0]}')

    def test_update_route(self):
        """Test update route for existing artifact object update"""
        response = self.client.post('/new', data=self.form)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.form['objectID'])
                             .first()
                             )
        response = self.client.post(f"/update/{self.form['objectID']}", data=self.updated_dict)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.form['objectID'])
                             .first())
        self.assertEqual(Artifact.query
                         .filter_by(objectID=self.form['objectID'])
                         .first()
                         .isHighlight, 'True')

    def test_integrity_error_duplicate_entry(self):
        """Test new route for duplicate object entry, assert IntegrityError"""
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query
                             .filter_by(objectID=self.artifact_fixture[0])
                             .first_or_404())

        with self.assertRaises(IntegrityError):
            self.client.post('/new', data=self.duplicate_dict)

    def test_server_error_duplicate_update_entry(self):
        """Test server error for duplicate update entry"""
        obj1 = Artifact(self.artifact_fixture)
        obj2 = Artifact(self.artifact_fixture1)
        db.session.add(obj1)
        db.session.add(obj2)
        with self.assertRaises(IntegrityError):
            self.client.post(f"/update/{self.artifact_fixture1[0]}", data=self.duplicate_dict)
