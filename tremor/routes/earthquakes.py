import json
from math import radians, cos, sin, asin, sqrt

from flask import Blueprint, request, Response

from datetime import datetime
from dateutil.tz import tzutc

from tremor.models import db, Record
from tremor import InvalidArgumentError

earthquakes = Blueprint('earthquakes', __name__)

@earthquakes.route('/earthquakes.json', methods=['GET'])
def get_earthquakes():
    query = db.session.query(Record);

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
    
    over = parse_over(request);    
    if over > 0:
        query = query.filter( Record.magnitude > over );

    query_results = query.all();

    results = [x.as_dict() for x in query_results];
    
    results = filter_near( results, request );

    return Response(response=json.dumps(results),
                    status=200,
                    mimetype="application/json");


def parse_on(request):
    
    if request.args.has_key('on'):
        try:
            on_datetime = datetime.fromtimestamp(int(request.args['on']), tzutc());
        except Exception as ex:
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

        return since_datetime;

    return None;

def parse_over(request):
    over = 0;
    if request.args.has_key('over'):
        try:
            over = float( request.args['over'] );
        except:
            raise InvalidArgumentError("Unable to parse 'over' parameter");

    return over;


def filter_near( results, request ):
    if request.args.has_key('near'):
        try:
            lat_lon_str = request.args['near'].split(',')
            lat, lon = float(lat_lon_str[0]), float(lat_lon_str[1])
        except:
            raise InvalidArgumentError("Unable to parse 'near' parameter")

        #   Using very small margin of error to accomodate for
        #       1. Floating point math
        #       2. Assuming Earth is a perfect sphere
        return [record for record in results if miles_between_gps_coordinates(lon, lat, record['lon'], record['lat']) <= 5.05];

    return results;

'''
    Mostly borrowed from :
    http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
'''
def miles_between_gps_coordinates(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula [http://en.wikipedia.org/wiki/Haversine_formula]
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    #
    #   3,959 mi is the radius of the Earth, assuming it is perfect sphere
    #       EARTH IS NOT A PERFECT SPHERE!
    return float("%.2f" % (3959 * c)) 