from dbmodules.base import BaseDBServer
from dbmodules.user import UserTable


class Server():

    @staticmethod
    def base_tips(reason, tips_type='info', *args, **kwargs):
        """ return response with code.
        if you want to use custom code,you can use code parameters
        """
        if 'info' == tips_type:
            code = 0
        elif "redirect" == tips_type:
            code = 2
        elif "warning" == tips_type:
            code = 1
        elif "error" == tips_type:
            code = -1
        else:
            code = kwargs.pop('code', -1)
        return {'code': code, 'msg': reason}

    def warning_tips(self, reason):
        return self.base_tips(reason, "warning")

    def error_tips(self, reason):
        return self.base_tips(reason, "error")

    def redirect_tips(self, reason):
        return self.base_tips(reason, "redirect")

