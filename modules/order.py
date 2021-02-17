from modules.server import Server
from modules.good import GoodServer
from dbmodules.base import CoreDBServer
from dbmodules.good import GoodTable
from dbmodules.order import OrderTable
from sqlalchemy import text
import datetime
import random
from com.pe_service_error import UNKNOW_ERROR
import logging
import copy


class OrderServer(Server):
    def __init__(self):
        self.dbser = CoreDBServer(OrderTable)
        super().__init__()

    def add_order(self, username: str, good_ids: list) -> dict:
        """return order detail or fail reason. """
        try:
            # 减库存
            ret = GoodServer().sub_inventory(good_ids)
            if 1 == ret['code']:
                return ret
            # 下单号 日期(精确到分) + 4位随机数，实际上要避免这种有明显规律的单号
            order_no = datetime.datetime.utcnow().strftime(
                '%Y%m%d%H%M')+str(random.randint(0, 9999)).zfill(4)
            good_id_str = ','.join([str(good_id) for good_id in good_ids])
            sql = "select price from %s where id in (%s);" % (
                GoodTable.name, good_id_str)
            rows = self.dbser.sql_execute(sql).fetchall()
            sum_price = sum([row[0] for row in rows])
            values = {"username": username, "order_no": order_no,
                      'good_ids': good_id_str, "sum_price": sum_price}
            self.dbser.insert(**values)
            return {'code': 0, 'order_no': order_no}
        except Exception as e:
            logging.error(e)
            return UNKNOW_ERROR

    def order_detail(self, username, order_no):
        wheres = [
            ["username", 'eq', username],
            ["order_no", 'eq', order_no]
        ]
        row = self.dbser.select(wheres).first()
        if row:
            order = self.dbser.row2json(row)
            # 15分钟过期
            end_time = copy.deepcopy(row['create_time'])
            end_time += datetime.timedelta(seconds=900)
            # 过期订单更新状态
            if datetime.datetime.now() > end_time and order['status'] not in (1, 3):
                order['status'] = 3
                GoodServer().release_inventory(order['good_ids'].split(','))
                print(self.dbser.update(wheres, status=3).rowcount)
            elif order['status'] in [0, 2]:
                order['exp_time'] = (
                    end_time-datetime.datetime.utcnow()).total_seconds()
            return {"code": 0, "order": order}
        else:
            return self.error_tips('订单不存在')

    def order_list(self, username, page, page_size):
        offset_num = (page-1) * page_size
        wheres = [
            ['username', 'eq', username]
        ]
        sorts_by = [
            ['create_time', '1']
        ]
        l = self.dbser.select(
            wheres, sorts_by, offset=offset_num, limit=page_size).fetchall()
        l = [self.dbser.row2json(i) for i in l]
        return {'code': 0, 'list': l}
