import sys, os, requests

from twisted.internet import reactor
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site

EXECUTE_EVERY = 60;
RAW_DATA_URL = 'http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M1.txt';

if __name__ == "__main__":

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
    
    from tremor import app, data_importer    
    
    port = int( os.environ.get('PORT', '5000'));
    resource = WSGIResource(reactor, reactor.getThreadPool(), app);
    reactor.listenTCP(port, Site(resource));

    '''
        Twisted plumbing
        execute_import creates a repeating task that is a best effort task.
        best effort meaning, if it fails we just try again in 'EXECUTE_EVERY' time

        It's using the built in twisted reactor to continually call the same method.
    '''
    def execute_import(*args, **kwargs):
        try:
            data_importer.parse_and_insert_data(requests.get(RAW_DATA_URL).text);
        except Exception:
            print(traceback.format_exc())

        reactor.callLater(EXECUTE_EVERY, execute_import);

    execute_import();
    reactor.run()
