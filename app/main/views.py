from flask import request, redirect, url_for, flash, render_template
from ..models import Artifact, keys
from .forms import EditArtifactForm
from io import TextIOWrapper
import csv

from . import main
from .. import db


@main.route('/', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        csv_file = request.files['file']
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
    artifacts = Artifact.query
    return render_template('table.html', title='Artifacts Table', artifacts=artifacts)


@main.route('/new', methods=['GET', 'POST'])
def new():
    form = EditArtifactForm(request.form)
    if form.validate_on_submit():
        row = []
        for key in keys:
            row.append(request.form[key])
        row = tuple(row)
        print(row)
        artifact = Artifact(row)
        db.session.add(artifact)
        db.session.commit()
        return redirect(url_for('.show'))
    return render_template('update_artifact.html', title='Add Artifact', form=form)


@main.route('/update/<object_id>', methods=['GET', 'POST'])
def update(object_id):
    artifact = Artifact.query.filter_by(objectID=object_id).first_or_404()
    form = EditArtifactForm(request.form, obj=artifact)
    print(request.form.to_dict())
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
    Artifact.query.filter_by(objectID=object_id).delete()
    db.session.commit()
    artifacts = Artifact.query
    return render_template('table.html', title='Artifacts Table', artifacts=artifacts)