from handlers.handle import BaseHandlers
from modules.order import OrderServer
from modules.order import GoodServer
from com.pe_service_error import UNKNOW_ERROR, LOCAL_FAIL_ERROR, PeException
import ast
from tornado.web import MissingArgumentError
import logging


class OrderHandler(BaseHandlers):
    def initialize(self, ser=None, *args, **kwargs):
        if ser:
            self.ser = ser
        else:
            self.ser = OrderServer()

    def post(self):
        suffix = self.request.uri.split('/')[-1].lower()
        if 'add' == suffix:
            return self.order_add()
        elif 'detail' == suffix:
            return self.order_detail()
        elif 'list' == suffix:
            return self.order_list()
        return self.finish(LOCAL_FAIL_ERROR)

    def order_add(self):
        try:
            username = self.is_login().get('username')
            good_ids = ast.literal_eval(self.get_body_argument('good_ids'))
            self.finish(self.ser.add_order(username, good_ids))
        except MissingArgumentError as e:
            self.finish({'code': 1, 'msg': '%s不能为空' % e.arg_name})
        except PeException as e:
            self.finish(e.reason)
        except Exception as e:
            logging.error(e)
            self.finish(UNKNOW_ERROR)

    def order_detail(self):
        try:
            username = self.is_login().get('username')
            order_no = self.get_body_argument('order_no')
            self.finish(self.ser.order_detail(username, order_no))
        except MissingArgumentError as e:
            self.finish({'code': 1, 'msg': '%s不能为空' % e.arg_name})
        except Exception as e:
            logging.error(e)
            self.finish(UNKNOW_ERROR)

    def order_list(self):
        try:
            username = self.is_login().get('username')
            page = int(self.get_body_argument('page', 0))
            page_size = int(self.get_body_argument('page_size', 0))
            self.finish(self.ser.order_list(username, page, page_size))
        except PeException as e:
            self.finish(e.reason)
        except MissingArgumentError as e:
            self.finish({'code': 1, 'msg': '%s不能为空' % e.arg_name})
        except Exception as e:
            logging.error(e)
            self.finish(UNKNOW_ERROR)
