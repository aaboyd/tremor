from app import app
from twisted.internet import reactor
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
import data_importer
import os

if __name__ == "__main__":

    port = int( os.environ.get('PORT', '5000'));

    resource = WSGIResource(reactor, reactor.getThreadPool(), app)

    site = Site(resource)

    reactor.listenTCP(port, site)

    print 'Listening on port : ' , port
    print 'Starting Server!'

    data_importer.start()
    reactor.run()
