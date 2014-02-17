from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet import defer
from twisted.web.client import getPage

from datetime import datetime
from dateutil.tz import tzutc
from sqlalchemy import func

import time, traceback, StringIO, csv, requests

from tremor import app
from tremor.models import db, Record

EXECUTE_EVERY = 60

'''
    Use CSV reader and parse the data and insert it into the database
'''
def parse_and_insert_data(data):
    f = StringIO.StringIO(data);

    reader = csv.reader(f)

    with app.app_context():
        
        most_recent_date = None;
        query = db.session.query(Record.datetime, func.max(Record.datetime).label('recent_date') );
        if query.count() == 1 and query.first()[0] is not None:
            most_recent_date = query.first().recent_date.replace(tzinfo=tzutc());

        i = 0;
        records_inserted = 0;
        for row in reader:

            # Ignore the first two lines
            #   Line 1 : Key
            #   Line 2 : Deprecation Warning
            if i < 2: i += 1; continue;

            # If the date is less than or equal to our most recent,
            # then we already have all these records
            if most_recent_date is not None and transform_date(row[3]) <= most_recent_date:
                break;

            record = create_record(row);
            db.session.add(record);
            records_inserted += 1;

        db.session.commit();


def transform_date(date_str):
    return datetime.strptime(date_str, '%A, %B %d, %Y %H:%M:%S %Z').replace(tzinfo=tzutc());


'''
    Ugly factory to take a CSV row and create a valid Record
'''
def create_record(row):
    return Record(src=row[0],
                  eqid=row[1],
                  version=int(row[2]),
                  datetime=transform_date(row[3]),
                  lat=float(row[4]),
                  lon=float(row[5]),
                  magnitude=float(row[6]),
                  depth=float(row[7]),
                  nst=int(row[8]),
                  region=row[9])
