import os, json, unittest

from datetime import datetime
from dateutil.tz import tzutc

from tremor import app, InvalidArgumentError
from tremor.data_importer import parse_and_insert_data
from tremor.routes.earthquakes import *

from util import MockRequest,\
    EARLY_DATA, EARLY_DATA_SIZE, LATER_DATA, LATER_DATA_SIZE, EXAMPLE_RESULTS

class Endpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client();
        parse_and_insert_data(EARLY_DATA);
        parse_and_insert_data(LATER_DATA);

    def test_default(self):
        response = self.app.get('/earthquakes.json');
        response_json_obj = json.loads( response.data );

        self.assertEqual(len(response_json_obj), EARLY_DATA_SIZE + LATER_DATA_SIZE );
        self.assertEqual(response.status_code, 200);

    def test_on_invalid(self):
        response = self.app.get('/earthquakes.json?on=jljasdk');
        response_json_obj = json.loads(response.data);

        self.assertEqual(response_json_obj['error'], "Unable to parse 'on' parameter");
        self.assertEqual(response.status_code, 400);

    def test_on(self):
        response = self.app.get('/earthquakes.json?on=1392546663');
        response_json_obj = json.loads( response.data );

        self.assertEqual(len(response_json_obj), LATER_DATA_SIZE);
        self.assertEqual(response.status_code, 200);

    def test_since_invalid(self):
        response = self.app.get('/earthquakes.json?since=jljasdk');
        response_json_obj = json.loads(response.data);

        self.assertEqual(response_json_obj['error'], "Unable to parse 'since' parameter");
        self.assertEqual(response.status_code, 400);

    def test_since(self):
        response = self.app.get('/earthquakes.json?since=1392503400');
        response_json_obj = json.loads( response.data );

        self.assertEqual(len(response_json_obj), 3 + LATER_DATA_SIZE );
        self.assertEqual(response.status_code, 200);

    def test_near_invalid(self):
        response = self.app.get('/earthquakes.json?near=jljasdk');
        response_json_obj = json.loads(response.data);

        self.assertEqual(response_json_obj['error'], "Unable to parse 'near' parameter");
        self.assertEqual(response.status_code, 400);

    def test_near(self):
        response = self.app.get('/earthquakes.json?near=32.7768,-115.3695');
        response_json_obj = json.loads(response.data);

        self.assertEqual(len(response_json_obj), 2);
        self.assertEqual(response.status_code, 200);

    def test_over_invalid(self):
        response = self.app.get('/earthquakes.json?over=jljasdk');
        response_json_obj = json.loads(response.data);

        self.assertEqual(response_json_obj['error'], "Unable to parse 'over' parameter");
        self.assertEqual(response.status_code, 400);

    def test_over(self):
        response = self.app.get('/earthquakes.json?over=2.0');
        response_json_obj = json.loads(response.data);

        self.assertEqual(len(response_json_obj), 5);
        self.assertEqual(response.status_code, 200);

    def test_on_and_since(self):
        response = self.app.get('/earthquakes.json?on=1392503100&since=1392503400');
        response_json_obj = json.loads(response.data);

        self.assertEqual(len(response_json_obj), 3);
        self.assertEqual(response.status_code, 200);