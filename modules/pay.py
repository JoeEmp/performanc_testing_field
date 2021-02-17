from modules.server import Server
from modules.order import OrderServer
from time import sleep
from dbmodules.order import OrderTable
from dbmodules.base import CoreDBServer
from com.pe_encrypt import random, ranstr


class PayServer(Server):

    def __init__(self):
        self.dbser = CoreDBServer(OrderTable)
        super().__init__()

    def pay(self, username, order_no):
        # 实际上应该还有第三方支付
        # 这里直接变更订单状态,没有单号校验
        # 模拟回调产生的消耗 200 +/- 50ms
        wheres = [
            ['order_no', 'eq', order_no],
        ]
        order = OrderServer().order_detail(username, order_no)
        if 0 == order['code']:
            status = order['order']['status']
        else:
            return order
        if 0 == status:
            sec = 0.2+random.randint(0, 50)*10**-3
            sleep(sec)
            values = {'status': 0}
            if 99999 > random.randint(0, 10**5):
                values['status'] = 1
                values['pay_id'] = 'wx'+ranstr()
            else:
                values['status'] = 2
            ret = self.dbser.update(wheres=wheres, **values).rowcount
            return {'code': 0, 'msg': '支付成功'}
        elif 3 == status:
            return {'code': 1, 'msg': "订单已过期"}
        elif 1 == status:
            return {'code': 1, 'msg': '订单已支付,请勿重复支付'}
