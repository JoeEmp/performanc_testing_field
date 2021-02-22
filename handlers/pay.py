from handlers.handle import BaseHandlers
from modules.pay import PayServer
from com.pe_service_error import UNKNOW_ERROR,PeException
import logging
from tornado.web import MissingArgumentError
from tornado import gen


class PayHandler(BaseHandlers):

    def initialize(self, ser=None, *args, **kwargs):
        if ser:
            self.ser = ser
        else:
            self.ser = PayServer()

    @gen.coroutine
    def post(self):
        try:
            username = self.is_login().get('username')
            order_no = self.get_argument('order_no')
            result = self.ser.pay(username, order_no)
        except PeException as e:
            logging.error(e.reason)
            result  = e.reason
        except MissingArgumentError as e:
            self.finish({'code': 1, 'msg': '%s不能为空' % e.arg_name})
        except Exception as e:
            logging.error(e)
            self.finish(UNKNOW_ERROR)
        # self.finish(result)
