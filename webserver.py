from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
import time

class ClockPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        with open ("html.txt", "r") as myfile:
            data=myfile.read()
        old = data.replace("sleepcycles", str(time.ctime()))
        return old

resource = ClockPage()
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run()