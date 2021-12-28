import unittest
from app import create_app, db
from app.models import Artifact
from fixtures.artifact import artifact_fixture, form_dict, updated_dict, duplicate_dict, artifact_fixture1


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
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
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_artifact_creation(self):
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404())

    def test_artifact_creation_when_obj_is_present(self):
        obj = Artifact(self.artifact_fixture)
        obj1 = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.add(obj1)
        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_artifact_updation(self):
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404())
        art = Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404()
        art.isHighlight = True
        db.session.add(art)
        db.session.commit()
        self.assertEqual(bool(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404().isHighlight),
                         True)

    def test_artifact_updation_duplicate_obj_id(self):
        obj = Artifact(self.artifact_fixture)
        obj1 = Artifact(self.artifact_fixture1)
        db.session.add(obj)
        db.session.add(obj1)
        db.session.commit()
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404())
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture1[0]).first_or_404())
        artifact1 = Artifact.query.filter_by(objectID=self.artifact_fixture1[0]).first_or_404()
        artifact1.objectID = artifact_fixture[0]
        db.session.add(artifact1)

        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_artifact_deletion(self):
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404())
        db.session.delete(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first())
        db.session.commit()
        self.assertIsNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first())

    def test_delete_non_existent(self):
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404())
        db.session.delete(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first())
        db.session.commit()
        from sqlalchemy.orm.exc import UnmappedInstanceError
        with self.assertRaises(UnmappedInstanceError):
            db.session.delete(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first())

    def test_create_route(self):
        response = self.client.post('/new', data=self.form)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.form['objectID']).first())

    def test_delete_route(self):
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404())
        response = self.client.get(f'/delete/{self.artifact_fixture[0]}')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first())

    def test_update_route(self):
        response = self.client.post('/new', data=self.form)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.form['objectID']).first())
        response = self.client.post(f"/update/{self.form['objectID']}", data=self.updated_dict)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.form['objectID']).first())
        self.assertEqual(Artifact.query.filter_by(objectID=self.form['objectID']).first().isHighlight, 'True')

    def test_integrity_error_duplicate_entry(self):
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404())

        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError):
            self.client.post('/new', data=self.duplicate_dict)

    def test_server_error_duplicate_update_entry(self):
        obj1 = Artifact(self.artifact_fixture)
        obj2 = Artifact(self.artifact_fixture1)
        db.session.add(obj1)
        db.session.add(obj2)
        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError):
            self.client.post(f"/update/{self.artifact_fixture1[0]}", data=self.duplicate_dict)






