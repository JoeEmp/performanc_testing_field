PARAMETERS_ERROR = {'code':-1,'msg':'参数错误'}
UNKNOW_ERROR = {'code':-1,'msg':'未知错误，请联系管理员'}
LOCAL_FAIL_ERROR = {'code':-1,'msg':'接口不存在'}
LOGIN_ERROR = {'code':2,'msg':'请重新登录'}


class PeException(BaseException):
    def __init__(self, reason, *args, **kwargs):
        self.reason = reason
        super().__init__(*args, **kwargs)
