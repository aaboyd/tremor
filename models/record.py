from . import db

class Record(db.Model):
    src = db.Column(db.String(2))
    eqid = db.Column(db.String(12), primary_key=True)
    version = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    magnitude = db.Column(db.Float)
    depth = db.Column(db.Float)
    nst = db.Column(db.Integer)
    region = db.Column(db.String(120))