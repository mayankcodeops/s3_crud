import os
import click

from app import create_app, db
from app.models import Artifact

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    """Returns a dict context to load on Flask shell"""
    return dict(db=db, Artifact=Artifact)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """
    Command to Run the unit tests
    Usage
        $ flask test # to run all the unit tests in the tests/folder
        $ flask test <test_name> to run a specific test
    """
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run()

