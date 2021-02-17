from tornado.web import RequestHandler
from com.pe_service_error import PeException, LOGIN_ERROR, PARAMETERS_ERROR, UNKNOW_ERROR
from com.pe_encrypt import sync_token
from dbmodules.user import UserTable
from time import time
import json
from dbmodules.base import BaseDBServer


class BaseHandlers(RequestHandler):

    def is_login(self):
        """return payload or raise PeException use handler error """
        token = self.request.headers.get('token', None)
        if token:
            ret = sync_token(token)
            if ret.get('exp', 0) > time() and self.is_legal_user(ret.get('username', '')):
                ret['code'] = 0
                return ret
        raise PeException(LOGIN_ERROR)

    def is_legal_user(self, username):
        sql = "select * from %s where username = %r" % (
            UserTable.name, username)
        return BaseDBServer().sql_execute(sql).first()

    def finish(self, chunk=None):
        if isinstance(chunk, dict):
            # self.add_header('Content-Type','application/json')
            chunk = json.dumps(chunk, ensure_ascii=False)
        return super().finish(chunk=chunk)
