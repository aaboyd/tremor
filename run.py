from twisted.internet import reactor
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site

import sys, os

if __name__ == "__main__":

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
    
    from tremor import app, data_importer    
    
    port = int( os.environ.get('PORT', '5000'));

    resource = WSGIResource(reactor, reactor.getThreadPool(), app)

    site = Site(resource)

    reactor.listenTCP(port, site)

    print 'Listening on port : ' , port
    print 'Starting Server!'

    data_importer.start()
    reactor.run()
