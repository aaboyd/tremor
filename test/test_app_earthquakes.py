import os, unittest

from tremor import app, InvalidArgumentError
from tremor.data_importer import transform_date, parse_and_insert_data
from tremor.models import db, Record
from tremor.routes.earthquakes import parse_on

from util import EARLY_DATA, EARLY_DATA_SIZE, LATER_DATA, LATER_DATA_SIZE

class TestEarthquakeParseOnParam(unittest.TestCase):

    def setUp(self):
        self.request = {};
        self.request.args = {};

    def test_missing(self):
        lower, upper = parse_on(self.request);

        self.assertIsNone( lower );
        self.assertIsNone( upper );

    def test_invalid(self):
        self.request.args['on'] = 'asdkjlkjfq';

        with self.assertRaises(InvalidArgumentError):
            parse_on( self.request );

    def test_day_start(self):
        self.assertTrue( False );

    def test_day_end(self):
        self.assertTrue( False );

    def test_day_mid(self):
        self.assertTrue( False );
    


def setUp(self):
    with app.app_context():
        db.session.query(Record).delete();
        db.session.commit();

def _insert_early(self):
    parse_and_insert_data(EARLY_DATA);
    return EARLY_DATA_SIZE;

def _insert_later(self):
    parse_and_insert_data(LATER_DATA);
    return LATER_DATA_SIZE;