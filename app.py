from io import TextIOWrapper
import csv

from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'hard-to-guess'
db = SQLAlchemy(app)

admin = Admin(app,name='users', template_mode='bootstrap3')


class User(db.Model):
    username = db.Column(db.String(80), unique=True)
    identifier = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))

    def __repr__(self):
        return "<User: {}>".format(self.username)


admin.add_view(ModelView(User, db.session))

keys = [
    "objectID",
    "isHighlight",
    "accessionNumber",
    "accessionYear",
    "isPublicDomain",
    "primaryImage",
    "primaryImageSmall",
    "department",
    "objectName",
    "title",
    "culture",
    "period",
    "dynasty",
    "reign",
    "portfolio",
    "artistRole",
    "artistPrefix",
    "artistDisplayName",
    "artistDisplayBio",
    "artistSuffix",
    "artistAlphaSort",
    "artistNationality",
    "artistBeginDate",
    "artistEndDate",
    "artistGender",
    "artistWikiDataURL",
    "artistULAN_URL",
    "objectDate",
    "objectBeginDate",
    "objectEndDate",
    "medium",
    "dimensions",
    "measurements",
    "creditLine",
    "geographyType",
    "city",
    "state",
    "county",
    "country",
    "region",
    "subregion",
    "locale",
    "locus",
    "excavation",
    "river",
    "classification",
    "rightsAndReproduction",
    "linkResource",
    "metadataDate",
    "repository",
    "objectURL",
    "tags",
    "objectDataWikiURL",
    "isTimeLineWork",
    "galleryNumber",
    "constituentID",
    "role",
    "name",
    "constituentULANURL",
    "constituentWikiDataURL",
    "gender",
]


class Artifact(db.Model):
    objectID = db.Column(db.String(10), primary_key=True)
    isHighlight = db.Column(db.String(50))
    accessionNumber = db.Column(db.String(50), unique=True)
    accessionYear = db.Column(db.String(50))
    isPublicDomain = db.Column(db.String(50))
    primaryImage = db.Column(db.Text)
    primaryImageSmall = db.Column(db.Text)
    department = db.Column(db.String(100))
    objectName = db.Column(db.String(50))
    title = db.Column(db.String(100))
    culture = db.Column(db.String(50))
    period = db.Column(db.String(100))
    dynasty = db.Column(db.String(100))
    reign = db.Column(db.String(100))
    portfolio = db.Column(db.String(100))
    artistRole = db.Column(db.String(50))
    artistPrefix = db.Column(db.String(50))
    artistDisplayName = db.Column(db.String(200))
    artistDisplayBio = db.Column(db.String(200))
    artistSuffix = db.Column(db.String(50))
    artistAlphaSort = db.Column(db.String(100))
    artistNationality = db.Column(db.String(50))
    artistBeginDate = db.Column(db.String(50))
    artistEndDate = db.Column(db.String(50))
    artistGender = db.Column(db.String(50))
    artistWikiDataURL = db.Column(db.String(200))
    artistULAN_URL = db.Column(db.String(200))
    objectDate = db.Column(db.String(100))
    objectBeginDate = db.Column(db.String(50))
    objectEndDate = db.Column(db.String(50))
    medium = db.Column(db.String(50))
    dimensions = db.Column(db.String(50))
    measurements = db.Column(db.Text)
    creditLine = db.Column(db.String(100))
    geographyType = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    county = db.Column(db.String(50))
    country = db.Column(db.String(50))
    region = db.Column(db.String(50))
    subregion = db.Column(db.String(50))
    locale = db.Column(db.String(50))
    locus = db.Column(db.String(50))
    excavation = db.Column(db.String(100))
    river = db.Column(db.String(50))
    classification = db.Column(db.String(50))
    rightsAndReproduction = db.Column(db.String(100))
    linkResource = db.Column(db.String(200))
    metadataDate = db.Column(db.String(50))
    repository = db.Column(db.String(100))
    objectURL = db.Column(db.String(100))
    tags = db.Column(db.Text)
    objectDataWikiURL = db.Column(db.String(200))
    isTimeLineWork = db.Column(db.String(50))
    galleryNumber = db.Column(db.String(50))
    constituentID = db.Column(db.String(50))
    role = db.Column(db.String(50))
    name = db.Column(db.String(100))
    constituentULANURL = db.Column(db.String(200))
    constituentWikiDataURL = db.Column(db.String(200))
    gender = db.Column(db.String(50))

    def __init__(self, row):
        for key, item in zip(keys, row):
            self.__dict__[key] = item


admin.add_view(ModelView(Artifact, db.session))


@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # user = User(username=row[0], identifier=row[1], firstname=row[2], lastname=row[3])
            print(row)
            artifact = Artifact(row)
            db.session.add(artifact)
            db.session.commit()
        return redirect(url_for('upload_csv'))
    return """
            <form method='post' action='/' enctype='multipart/form-data'>
              Upload a csv file: <input type='file' name='file'>
              <input type='submit' value='Upload'>
            </form>
           """


@app.route('/show')
def show():
    users = User.query
    return render_template('table.html', title='User Table', users=users)


if __name__ == '__main__':
    db.create_all()
    app.run()

