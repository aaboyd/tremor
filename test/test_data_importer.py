import os, unittest

from dateutil.tz import tzutc
from datetime import datetime

from sqlalchemy import func

from tremor import app
from tremor.data_importer import transform_date, parse_and_insert_data
from tremor.models import db, Record

from util import EARLY_DATA, EARLY_DATA_SIZE, LATER_DATA, LATER_DATA_SIZE

class TestTransformDate(unittest.TestCase):
    def test_data_importer_transform_date(self):
        control = datetime(2014, 2, 22, 2, 2, 22, 0, tzinfo=tzutc());

        self.assertEqual( transform_date('Saturday, February 22, 2014 02:02:22 UTC'), control );

class TestDataImporter(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            db.session.query(Record).delete();
            db.session.commit();

    def test_basic_insert(self):
        before = self._get_db_rows();
        
        rows_in_data = self._insert_early();
        
        after = self._get_db_rows();

        self.assertEqual( rows_in_data , after - before );

    def test_multiple_insert(self):
        before = self._get_db_rows();
        
        rows_in_data = self._insert_early();
        rows_in_data += self._insert_later();

        after = self._get_db_rows();

        self.assertEqual( rows_in_data , after - before );

    def test_earlier_date_insert(self):
        before = self._get_db_rows();
        
        rows_in_data = self._insert_later();
        self._insert_early();

        after = self._get_db_rows();

        self.assertEqual( rows_in_data , after - before );

    def _insert_early(self):
        parse_and_insert_data(EARLY_DATA);
        return EARLY_DATA_SIZE;

    def _insert_later(self):
        parse_and_insert_data(LATER_DATA);
        return LATER_DATA_SIZE;

    def _get_db_rows(self):
        num_records = 0;
        with app.app_context():
            num_records = len(db.session.query(Record).all());

        return num_records
    