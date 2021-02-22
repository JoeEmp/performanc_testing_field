from modules.server import Server
from dbmodules.base import CoreDBServer
from dbmodules.user import UserTable
from com.pe_encrypt import get_token
import logging
from com.pe_service_error import PeException, UNKNOW_ERROR


class LoginServer(Server):
    def __init__(self):
        self.dbser = CoreDBServer(UserTable)
        super().__init__()

    def login(self, username, password):
        """return token or error msg. """
        wheres = [
            ["username", 'eq', username]
        ]
        row = self.dbser.select(wheres).first()
        if not row:
            logging.warning(
                'username:{} password:{} 用户不存在'.format(username, password))
            return self.error_tips("不存在该用户")
        if password == row['password']:
            return {'code': 0, 'token': get_token(username)}
        elif password != row['password']:
            logging.warning(
                'username:{} password:{} 密码错误'.format(username, password))
            return self.error_tips('密码错误')
        else:
            return self.error_tips('未知错误')
