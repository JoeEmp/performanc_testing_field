from handlers.handle import BaseHandlers
from modules.pay import PayServer
from com.pe_service_error import UNKNOW_ERROR
import logging
from tornado.web import MissingArgumentError


class PayHandler(BaseHandlers):

    def initialize(self, ser=None, *args, **kwargs):
        if ser:
            self.ser = ser
        else:
            self.ser = PayServer()

    def post(self):
        try:
            username = self.is_login().get('username')
            order_no = self.get_argument('order_no')
            result = self.ser.pay(username, order_no)
        except MissingArgumentError as e:
            self.finish({'code': 1, 'msg': '%s不能为空' % e.arg_name})
        except Exception as e:
            logging.error(e)
            result = UNKNOW_ERROR
        self.finish(result)
