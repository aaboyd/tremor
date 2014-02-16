from flask import Blueprint, request
import json

from tremor.models import db, Record
from tremor import InvalidArgumentError

earthquakes = Blueprint('earthquakes', __name__)

@earthquakes.route('/earthquakes.json', methods=['GET'])
def get_earthquakes():
    query = db.session.query(Record);

    lower_bound = None;
    upper_bound = None;

    lower_bound, upper_bound = parse_on(request);

    since_lower = parse_since(request);

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


def parse_on(request):
    
    if request.args.has_key('on'):
        try:
            on_datetime = datetime.fromtimestamp(int(request.args['on']), tzutc());
        except:
            raise InvalidArgumentError("Unable to parse 'on' parameter")

        return on_datetime.replace(hour=0, minute=0, second=0, microsecond=0),\
            on_datetime.replace(hour=23, minute=59, second=59, microsecond=59);
    
    return None, None;

def parse_since(request):

    if request.args.has_key('since'):
        try:
            since_datetime = datetime.fromtimestamp(int(request.args['since']), tzutc());
        except:
            raise InvalidArgumentError("Unable to parse 'since' parameter");

        return since_datetime.fromtimestamp(int(request.args['since']), tzutc());

    return None;