from . import db

class Record(db.Model):
    Src = db.Column(db.String(2))
    Eqid = db.Column(db.Integer)
    Version = db.Column(db.Integer)
    Datetime = db.Column(db.DateTime, primary_key=True)
    Lat = db.Column(db.Float)
    Lon = db.Column(db.Float)
    Magnitude = db.Column(db.Float)
    Depth = db.Column(db.Float)
    NST = db.Column(db.Integer)
    Region = db.Column(db.String(120))


