from tornado.web import MissingArgumentError, RequestHandler, asynchronous
from modules.login import LoginServer
from com.pe_service_error import PeException, UNKNOW_ERROR
from tornado.gen import coroutine,sleep
import logging
import random
from tornado.httpclient import AsyncHTTPClient
# from time import sleep


class LoginHandler(RequestHandler):

    def initialize(self, ser=None, *args, **kwargs):
        if ser:
            self.ser = ser
        else:
            self.ser = LoginServer()

    @asynchronous
    @coroutine
    def post(self):
        try:
            password = self.get_body_argument('password')
            username = self.get_body_argument('username')
            result = self.ser.login(username, password)
            # yield sleep(5)
            # AsyncHTTPClient().fetch('http://www.baidu.com')
            self.finish(result)
        except MissingArgumentError as e:
            self.finish({'code': 1, 'msg': '%s不能为空' % e.arg_name})
        except Exception as e:
            logging.error(e)
            self.finish(UNKNOW_ERROR)
