import unittest
from app import create_app, db
from app.models import Artifact
from fixtures.artifact import artifact_fixture


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # TODO insert data from Artifact
        self.artifact_fixture = artifact_fixture

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # TODO insert test case scenarios
    def test_artifact_creation(self):
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404())

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

    def test_artifact_deletion(self):
        obj = Artifact(self.artifact_fixture)
        db.session.add(obj)
        db.session.commit()
        self.assertIsNotNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first_or_404())
        db.session.delete(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first())
        db.session.commit()
        self.assertIsNone(Artifact.query.filter_by(objectID=self.artifact_fixture[0]).first())

