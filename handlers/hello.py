from tornado.web import RequestHandler
from tornado import gen

class HelloHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        who = self.get_argument("who",default='joe')
        self.render('hello.html',who=who)