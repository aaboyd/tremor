import os, unittest

from datetime import datetime
from dateutil.tz import tzutc

from tremor import app, InvalidArgumentError
from tremor.routes.earthquakes import *

from util import MockRequest,\
    EARLY_DATA, EARLY_DATA_SIZE, LATER_DATA, LATER_DATA_SIZE, EXAMPLE_RESULTS

class ParseOnParam(unittest.TestCase):

    def setUp(self):
        self.request = MockRequest();

    def test_missing(self):
        lower, upper = parse_on(self.request);

        self.assertIsNone( lower );
        self.assertIsNone( upper );

    def test_invalid(self):
        self.request.args['on'] = 'asdkjlkjfq';

        with self.assertRaises(InvalidArgumentError):
            parse_on( self.request );

    def test_day_start(self):
        self.request.args['on'] = '1393027200';
        expected_lower = datetime(2014, 02, 22, 0, 0, 0, tzinfo=tzutc() );
        expected_upper = datetime(2014, 02, 22, 23, 59, 59, 59, tzinfo=tzutc() );

        lower_bound, upper_bound = parse_on( self.request );

        self.assertEqual( lower_bound, expected_lower );
        self.assertEqual( upper_bound, expected_upper );

    def test_day_end(self):
        self.request.args['on'] = '1393113599'
        expected_lower = datetime(2014, 02, 22, 0, 0, 0, tzinfo=tzutc() );
        expected_upper = datetime(2014, 02, 22, 23, 59, 59, 59, tzinfo=tzutc() );

        lower_bound, upper_bound = parse_on( self.request );

        self.assertEqual( lower_bound, expected_lower );
        self.assertEqual( upper_bound, expected_upper );

    def test_day_mid(self):
        self.request.args['on'] = '1393064421'
        expected_lower = datetime(2014, 02, 22, 0, 0, 0, tzinfo=tzutc() );
        expected_upper = datetime(2014, 02, 22, 23, 59, 59, 59, tzinfo=tzutc() );

        lower_bound, upper_bound = parse_on( self.request );

        self.assertEqual( lower_bound, expected_lower );
        self.assertEqual( upper_bound, expected_upper );
    

class ParseSinceParam(unittest.TestCase):

    def setUp(self):
        self.request = MockRequest();

    def test_missing(self):
        self.assertIsNone( parse_since( self.request ) );

    def test_invalid(self):
        self.request.args['since'] = 'asdfasdf';
        with self.assertRaises(InvalidArgumentError):
            parse_since(self.request);

    def test_valid(self):
        self.request.args['since'] = '1393064421';
        self.assertEqual( parse_since( self.request ), datetime(2014, 02, 22, 10, 20, 21, tzinfo=tzutc() ) );


class ParseOverParam(unittest.TestCase):

    def setUp(self):
        self.request = MockRequest();

    def test_missing(self):
        self.assertEqual( parse_over( self.request ), 0 );

    def test_invalid(self):
        self.request.args['over'] = 'asdfkji';
        with self.assertRaises(InvalidArgumentError):
            parse_over(self.request);

    def test_valid(self):
        self.request.args['over'] = '2.0';
        self.assertEqual( parse_over( self.request ), 2.0 );
        
        self.request.args['over'] = '3.4';
        self.assertEqual( parse_over( self.request ), 3.4 );


class FilterNearParam(unittest.TestCase):

    def setUp(self):
        self.request = MockRequest();

    def test_missing_param_no_results(self):
        self.assertEqual([], filter_near([], self.request) );

    def test_missing_param(self):
        self.assertEqual(EXAMPLE_RESULTS, filter_near(EXAMPLE_RESULTS, self.request) );

    def test_invalid(self):
        self.request.args['near'] = 'NOT_GOING_TO_WORK';
        with self.assertRaises(InvalidArgumentError):
            filter_near(EXAMPLE_RESULTS, self.request);

    def test_valid(self):
        self.request.args['near'] = '34.0263,-116.732';
        results = filter_near(EXAMPLE_RESULTS, self.request);
        self.assertEqual(len(results), 1);

        self.request.args['near'] = '33.266,-116.392';
        results = filter_near(EXAMPLE_RESULTS, self.request);
        self.assertEqual(len(results), 1);

        

class MilesBetweenPoints(unittest.TestCase):

    '''
        Estimates calculated with [http://www.gpsvisualizer.com/calculators]
    '''
    def test_valid_coordinates(self):
        MARGIN_OF_ERROR = 0.0025;

        mb = miles_between_gps_coordinates;

        expected = 55.911;
        result = mb(-116.732, 34.0263, -116.3924, 33.2663);
        self.assertAlmostEqual(result, expected, delta=expected*MARGIN_OF_ERROR );

        expected = 3214.263
        result = mb(-116.3565, 33.3712, -67.1054, 18.058)
        self.assertAlmostEqual( result, expected, delta=expected*MARGIN_OF_ERROR )
        
        expected = 44.71
        result = mb(-116.5762, 33.4995, -116.2708, 32.9037)
        self.assertAlmostEqual(result, expected, delta=expected*MARGIN_OF_ERROR )

        expected = 311.68
        result = mb(-118.9687, 37.6142, -116.0692, 33.7608)
        self.assertAlmostEqual(result, expected, delta=expected*MARGIN_OF_ERROR )