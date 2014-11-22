'''from twisted.internet import reactor
from twisted.internet import task
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet.protocol import Protocol, Factory

import time

class Echo(Protocol):
    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        self.transport.write(data)

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


from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server
from twisted.web.resource import Resource
import time
 
class ClockPage(Resource):
    isLeaf = True
    def __init__(self):
        self.presence=[]
        loopingCall = task.LoopingCall(self.__print_time)
        loopingCall.start(1, False)
        Resource.__init__(self)
     
    def render_GET(self, request):
        request.write('<b>%s</b><br>' % (time.ctime(),))
        self.presence.append(request)
        return server.NOT_DONE_YET
     
    def __print_time(self):
        for p in self.presence:
            p.write('<b>%s</b><br>' % (time.ctime(),))
 
resource = ClockPage()
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run() 
'''

from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server
from twisted.web.resource import Resource
import time
 
class ClockPage(Resource):
    isLeaf = True
    def __init__(self):
        self.presence=[]
        loopingCall = task.LoopingCall(self.__print_time)
        loopingCall.start(1, False)
        Resource.__init__(self)
     
    def render_GET(self, request):
        with open ("html.txt", "r") as myfile:
            data=myfile.read()
        old = data.replace("sleepcycles", str(time.ctime()))
        request.write(old)
        self.presence.append(request)
        return server.NOT_DONE_YET

     
    def __print_time(self):
        self.presence.remove(p)
        
        for p in self.presence:
            with open ("html.txt", "r") as myfile:
                data=myfile.read()
            old = data.replace("sleepcycles", str(time.ctime()))
            p.write(old)
 
resource = ClockPage()
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run() 