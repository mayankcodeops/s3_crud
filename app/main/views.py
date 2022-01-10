from flask import request, redirect, url_for, flash, render_template
from ..models import Artifact, keys
from .forms import EditArtifactForm
from io import TextIOWrapper
import csv

from . import main
from .. import db


@main.route('/', methods=['GET', 'POST'])
def upload_csv():
    """Route for Uploading CSV file"""
    if request.method == 'POST':
        csv_file = request.files['file']
        # TODO Save it to AWS EBS/EFS
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            artifact = Artifact(row)
            db.session.add(artifact)
            db.session.commit()
        return redirect(url_for('.upload_csv'))
    return render_template('upload.html', title='CSV Viewer')


@main.route('/show')
def show():
    """Route to display datatable from database records"""
    artifacts = Artifact.query
    return render_template('table.html', title='Artifacts Table', artifacts=artifacts)


@main.route('/new', methods=['GET', 'POST'])
def new():
    """Route for creating New Artifact object"""
    form = EditArtifactForm(request.form)
    if form.validate_on_submit():
        # TODO store the row as a S3 bucket object
        row = []
        for key in keys:
            row.append(request.form[key])
        row = tuple(row)
        artifact = Artifact(row)
        db.session.add(artifact)
        db.session.commit()
        return redirect(url_for('.show'))
    return render_template('update_artifact.html', title='Add Artifact', form=form)


@main.route('/update/<object_id>', methods=['GET', 'POST'])
def update(object_id):
    """Route for updating any artifact object"""
    # TODO fetch the s3 object from the bucket to update it
    artifact = Artifact.query.filter_by(objectID=object_id).first_or_404()
    form = EditArtifactForm(request.form, obj=artifact)
    if form.validate_on_submit():
        form.populate_obj(artifact)
        db.session.add(artifact)
        db.session.commit()
        flash('Artifact Updated')
        return redirect(url_for('.show'))
    for key in keys:
        setattr(form, key, artifact.__dict__[key])
    return render_template('update_artifact.html', title='Edit Artifact', form=form)


@main.route('/delete/<object_id>', methods=['GET', 'POST'])
def delete(object_id):
    """Route for deleting any existing artifact object"""
    # TODO delete the particular S3 object
    db.session.delete(Artifact.query.filter_by(objectID=object_id).first())
    db.session.commit()
    artifacts = Artifact.query
    return render_template('table.html', title='Artifacts Table', artifacts=artifacts)
