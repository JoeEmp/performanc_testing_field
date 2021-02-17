import requests
from settings import PORT
from dbmodules.base import CoreDBServer
from dbmodules.user import UserTable
from dbmodules.order import OrderTable
import logging


def pe_api(url, data=None, headers=None):
    try:
        ret = requests.post(url, headers=headers, data=data)
        # print(ret.request.headers, ret.request.body)
        return ret.json()
    except requests.exceptions.ConnectionError as e:
        print('网络错误')
        return
    except Exception as e:
        return (ret.request.headers, ret.request.body, ret.text)


def login():
    row = CoreDBServer(UserTable).select().first()
    data = {
        'username': row['username'],
        'password': row['password']
    }
    return pe_api('http://localhost:%s/jmeter/login' % PORT, data=data)


def exp_order(order_no):
    """过期订单(有效期为15分钟)."""
    sql = 'update %s set create_time = date_sub(create_time, interval 15 minute)  where order_no = %r' % (
        OrderTable.name, order_no)
    CoreDBServer().sql_execute(sql)
