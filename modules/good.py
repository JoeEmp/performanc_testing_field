from modules.server import Server
from dbmodules.base import CoreDBServer
from dbmodules.good import GoodTable
from com.pe_service_error import UNKNOW_ERROR
from sqlalchemy.engine.result import ResultProxy
import logging
from sqlalchemy import text


class GoodServer(Server):
    def __init__(self):
        self.dbser = CoreDBServer(GoodTable)
        super().__init__()

    def app_goods_list(self, page, page_size, sorts_by, *args, **kwargs):
        offset, limit = page, page_size
        if offset >= 1:
            offset = (offset-1) * limit
        else:
            limit = 0
        wheres = [['inventory', 'gt', '0'], ]
        rows = self.dbser.select(wheres, sorts_by, offset, limit).fetchall()
        return {'code': 0, "list": [self.dbser.row2json(row) for row in rows]}

    def good_detail(self, id):
        try:
            wheres = [['id', 'eq', id]]
            row = self.dbser.select(wheres).first()
            if not row:
                return self.error_tips('商品不存在')
            else:
                return {'code': 0, "good": self.dbser.row2json(row)}
        except Exception as e:
            logging.error(e)
            return UNKNOW_ERROR

    def release_inventory(self, ids: list):
        """rlease inventory when order exp。"""
        good_id_str = ','.join([str(good_id) for good_id in ids])
        sql = """update %s set inventory = inventory+1 where id in (%s); """ % (
            self.dbser.table.name, good_id_str)
        return self.dbser.sql_transaction_execute(sql=sql)

    def sub_inventory(self, ids: list) -> dict:
        """sub inventory when order add. """
        good_id_str = ','.join([str(good_id) for good_id in ids])
        sql = """update %s set inventory = inventory-1 where id in (%s) and inventory >0 ; """ % (
            self.dbser.table.name, good_id_str)
        conn = self.dbser.connect()
        with conn.begin() as tran:
            if len(ids) == conn.execute(sql).rowcount:
                tran.commit()
                return {'code': 0}
            else:
                tran.rollback()
                return {'code': 1, 'msg': '库存不足'}
