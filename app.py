from flask import Flask, request
from sqlalchemy.ext.declarative import DeclarativeMeta
import os, json

from models import db, Record
from datetime import datetime
from dateutil.tz import tzutc


app = Flask(__name__)
app.config.from_object('settings.base');

if os.environ.get('FLASK_CONFIG') is not None:
    app.config.from_object(os.environ.get('FLASK_CONFIG'));

db.init_app(app)

with app.app_context():
    db.create_all();

class InvalidArgumentError(Exception):
    pass;

@app.errorhandler(InvalidArgumentError)
def handle_sqlalchemy_assertion_error(err):
    return json.dumps(error=err.message), 400;

@app.route('/earthquakes.json')
def earthquakes():
    query = db.session.query(Record);

    lower_bound = None;
    upper_bound = None;

    lower_bound, upper_bound = parse_on(query);

    since_lower = parse_since(query);

    if since_lower is not None and lower_bound is not None and since_lower > lower_bound:
        lower_bound = since_lower;
    elif lower_bound is None and since_lower is not None:
        lower_bound = since_lower;

    if lower_bound is not None:
        query = query.filter( Record.datetime >= lower_bound );

    if upper_bound is not None:
        query = query.filter( Record.datetime < upper_bound );
    
    if request.args.has_key('over'):
        query = query.filter( Record.magnitude > int(request.args['over']) );

    results = query.all();

    results_as_dicts = [x.as_dict() for x in results];
    
    if request.args.has_key('near'):
        pass;

    return json.dumps(results_as_dicts);


def parse_on(query):
    
    if request.args.has_key('on'):
        try:
            on_datetime = datetime.fromtimestamp(int(request.args['on']), tzutc());
        except:
            raise InvalidArgumentError()

        return on_datetime.replace(hour=0, minute=0, second=0, microsecond=0),\
            on_datetime.replace(hour=23, minute=59, second=59, microsecond=59);
    
    return None, None;

def parse_since(query):

    if request.args.has_key('since'):
        try:
            since_datetime = datetime.fromtimestamp(int(request.args['since']), tzutc());
        except:
            raise InvalidArgumentError("Unable to parse 'since' parameter"), 400;

        return since_datetime.fromtimestamp(int(request.args['since']), tzutc());

    return None;
