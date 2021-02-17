import os
from urls import *
import settings
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpserver import HTTPServer


def make_app(is_debug=False):
    return Application(
        url_patterns,
        template_path=os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'templates'),
        debug=is_debug
    )


def main():
    app = make_app()
    server = HTTPServer(app)
    server.bind(settings.PORT)
    server.start(0)  # forks one process per cpu with debug == False
    IOLoop.current().start()


def debug_main():
    app = make_app(is_debug=True)
    app.listen(settings.PORT)
    IOLoop.current().start()


if __name__ == "__main__":
    import sys
    print('http://localhost:%s/' % settings.PORT)
    if len(sys.argv) >= 2 and sys.argv[1] == 'debug':
        debug_main()
    else:
        main()
