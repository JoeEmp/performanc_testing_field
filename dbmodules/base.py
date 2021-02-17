from sqlalchemy import text, event, delete, select, update, desc
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine.result import ResultProxy, RowProxy
from com.pe_database import ENGINE
import logging
from datetime import datetime
from contextlib import contextmanager


def transaction(func):
    def wrapper(self, *args, **kwargs):
        try:
            conn = self.connect()
            with conn.begin():
                return func(self, conn, *args, **kwargs)
        except Exception as e:
            logging.error(e)
    return wrapper


class BaseDBServer():
    option = {
        "eq": '=',
        "ne": '!=',
        'lt': '<',
        'gt': ">",
        'le': '<=',
        'ge': '>=',
        '1': 'desc',
        '0': 'asc'
    }

    @staticmethod
    def connect() -> Connection:
        return ENGINE.connect()

    @staticmethod
    def row2json(row: RowProxy) -> dict:
        """deal datetime to json error. """
        keys, values = row.keys(), row.values()
        new_row = {}
        try:
            for i in range(len(keys)):
                if isinstance(values[i], datetime):
                    values[i] = datetime.strftime(
                        values[i], '%Y-%m-%d %H:%M:%S')
                new_row[keys[i]] = values[i]
        except Exception as e:
            logging.error(e)
        return new_row

    @ staticmethod
    def row2dict(orm_row):
        d = {}
        for key, value in orm_row.__dict__.items():
            if '_sa_instance_state' == key:
                continue
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            d[key] = value
        return d

    def sql_execute(self, sql, param=None, conn=None) -> ResultProxy:
        if not isinstance(sql, tuple) and not isinstance(sql, list):
            sql = [sql]
        if param and not isinstance(param, tuple) and not isinstance(param, list):
            param = [param]
        if not conn:
            conn = self.connect()
        for i in range(len(sql)):
            if param:
                ret = conn.execute(text(sql[i]).params(param[i]))
            else:
                ret = conn.execute(text(sql[i]))
        return ret

    @transaction
    def sql_transaction_execute(self, conn, sql, param=None) -> ResultProxy:
        return self.sql_execute(sql, param, conn)


class CoreDBServer(BaseDBServer):
    """可进行简单的单表事务,和多表查询.
    https://www.osgeo.cn/sqlalchemy/core/dml.html"""

    def __init__(self, table=None):
        self.table = table

    @transaction
    def dml_transaction(self, conn, dml_obj, *args) -> ResultProxy:
        return self.dml_execute(dml_obj, conn, *args)

    def dml_execute(self, dml_obj, conn=None, data_list=[], *args, **kwargs) -> ResultProxy:
        try:
            if not conn:
                conn = self.connect()
            if data_list:
                return conn.execute(dml_obj, data_list)
            else:
                return conn.execute(dml_obj)
        except Exception as e:
            logging.error(e)

    def insert(self, *args, **kwargs) -> ResultProxy:
        insert_dml = self.table.insert().values(**kwargs)
        return self.dml_transaction(dml_obj=insert_dml)

    def many_insert(self, data_list) -> ResultProxy:
        insert_dml_temp = self.table.insert()
        return self.dml_execute(dml_obj=insert_dml_temp, data_list=data_list)

    def clear(self) -> ResultProxy:
        return self.dml_execute(delete(self.table))

    def update(self, wheres=[], table=None, **values):
        table = table or self.table
        where_texts = []
        for w in wheres:
            where_texts.append("%s %s %r" % (w[0], self.option[w[1]], w[2]))
        wt = ' AND '.join(where_texts)
        upt = table.update().where(text(wt)).values(**values)
        return self.dml_execute(upt, is_transaction=True)

    def select(self, wheres=[], sorts_by=[], offset=0, limit=1, tables=None) -> ResultProxy:
        """注意,过滤均为and. """
        s = select(tables or [self.table])
        s = s.offset(offset).limit(limit)
        for w in wheres:
            s = s.where(text("%s %s %r" % (w[0], self.option[w[1]], w[2])))
        for sort in sorts_by:
            if '1' == sort[1]:
                s = s.order_by(desc(sort[0]))
            elif '0' == sort[1]:
                s = s.order_by(sort[0])
        logging.debug(s)
        return self.connect().execute(s)
