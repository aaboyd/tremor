from . import db

from dateutil.tz import tzutc
from time import mktime

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

    def as_dict(self):
        return {'src':self.src,
                'eqid':self.eqid,
                'version':self.version,
                'datetime':int(mktime(self.datetime.replace(tzinfo=tzutc()).timetuple())),
                'lat':self.lat,
                'lon':self.lon,
                'magnitude':self.magnitude,
                'depth':self.depth,
                'nst':self.nst,
                'region':self.region};