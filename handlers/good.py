from handlers.handle import BaseHandlers
from modules.good import GoodServer
import logging
from com.pe_service_error import UNKNOW_ERROR
from tornado.web import MissingArgumentError
import ast

class GoodHandler(BaseHandlers):
    def initialize(self, ser=None, *args, **kwargs):
        if ser:
            self.ser = ser
        else:
            self.ser = GoodServer()

    def post(self):
        suffix = self.request.uri.split('/')[-1]
        if 'list' == suffix:
            return self.goods_list()
        elif 'detail' == suffix:
            return self.good_detail()
        return self.finish(UNKNOW_ERROR)

    def goods_list(self):
        try:
            page = int(self.get_body_argument('page', 0))
            page_size = int(self.get_body_argument('page_size', 0))
            sorts_by = ast.literal_eval((self.get_body_argument('sorts_by', '[]')))
            result = self.ser.app_goods_list(page, page_size,sorts_by)
        except Exception as e:
            logging.error(e)
            result = UNKNOW_ERROR
        self.finish(result)

    def good_detail(self):
        try:
            id = self.get_body_argument('id')
            self.finish(self.ser.good_detail(id))
        except MissingArgumentError as e:
            self.finish({'code': 1, 'msg': '%s不能为空' % e.arg_name})
