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
from twisted.web import server, rewrite, resource
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
            rewrite.RewriterResource(p, rewrite.tildeToUsers)

class RewriterResource(resource.Resource):
    def __init__(self, orig, *rewriteRules):
        resource.Resource.__init__(self)
        self.resource = orig
        self.rewriteRules = list(rewriteRules)

    def _rewrite(self, request):
        for rewriteRule in self.rewriteRules:
           rewriteRule(request)

    def getChild(self, path, request):
        request.postpath.insert(0, path)
        request.prepath.pop()
        self._rewrite(request)
        path = request.postpath.pop(0)
        request.prepath.append(path)
        return self.resource.getChildWithDefault(path, request)

    def render(self, request):
        self._rewrite(request)
        return self.resource.render(request)
        
    def tildeToUsers(request):
        if request.postpath and request.postpath[0][:1]=='~':
            request.postpath[:1] = ['users', request.postpath[0][1:]]
            request.path = '/'+'/'.join(request.prepath+request.postpath)
 
resource = ClockPage()
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run() 