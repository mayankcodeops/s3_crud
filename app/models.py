from . import db
import json

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
    """
    Database Model for the Museum Artifact
    """
    objectID = db.Column(db.String(10), primary_key=True)
    isHighlight = db.Column(db.String(50))
    accessionNumber = db.Column(db.String(50))
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
        """Initialize artifact object from a CSV record tuple"""
        for key, item in zip(keys, row):
            self.__dict__[key] = item

    @staticmethod
    def export_json(row):
        """Return a JSON serializable for an artifact object"""
        obj = {}
        for key, item in zip(keys, row):
            obj[key] = item

        return json.dumps(obj)

    @staticmethod
    def import_json(obj):
        """Creates an artifact object from a JSON"""
        obj = json.loads(obj)
        return tuple(obj.values())
