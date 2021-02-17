import unittest
import sys
import os
from time import sleep
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.sep.join(root_dir.split(os.sep)[:-1]))
from settings import PORT
from con_api import login, requests, exp_order, pe_api

class order_api(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = login()['token']
        return super().setUpClass()

    def test_visitor_order_add(self):
        """游客下单商品."""
        data = {
            "good_ids": '[3]'
        }
        ret = requests.post(
            "http://localhost:%s/jmeter/app/order/add" % PORT, data=data).json()
        self.assertEqual(2, ret['code'], ret)

    def test_signal_good_order(self):
        """单个商品下单"""
        good_ids_str = '[3]'
        ret = self.order_add(good_ids_str)
        self.assertIn('order_no', ret.keys(), ret)

    def test_many_good_order(self):
        """多个商品下单"""
        good_ids_str = '[3,2]'
        ret = self.order_add(good_ids_str)
        self.assertIn('order_no', ret.keys(), ret)

    def test_order_detail(self):
        """订单详情接口"""
        good_ids_str = '[3,2]'
        order_no = self.order_add(good_ids_str)['order_no']
        ret = self.order_detail(order_no)
        self.assertIn('order', ret.keys(), ret)

    def test_exp_order_detail(self):
        """过期订单查询 """
        good_ids_str = '[3,2]'
        order_no = self.order_add(good_ids_str)['order_no']  # 操作库过期订单
        exp_order(order_no)
        ret = self.order_detail(order_no)
        status = ret['order']['status']
        self.assertEqual(3, status, ret)

    def test_not_exist_order_detail(self):
        order_no = '123'
        ret = self.order_detail(order_no)
        self.assertIn('订单不存在', ret['msg'], ret)

    def test_order_list(self):
        """订单列表"""
        # 在并发处理的情况下可能不是最新的订单,生产环境是多线程的并不适用
        sleep(1)
        good_ids_str = '[3,2]'
        order_no = self.order_add(good_ids_str)['order_no']  # 操作库过期订单
        ret = self.order_list(page=1, page_size=1)
        self.assertEqual(order_no, ret['list'][0]['order_no'], ret)

    def order_add(self, good_ids_str):
        data = {
            "good_ids": good_ids_str
        }
        headers = {'token': self.token}
        return pe_api(
            "http://localhost:%s/jmeter/app/order/add" % PORT, headers=headers, data=data)

    def order_detail(self, order_no):
        data = {"order_no": order_no}
        headers = {'token': self.token}
        return pe_api(
            "http://localhost:%s/jmeter/app/order/detail" % PORT, headers=headers, data=data)

    def order_list(self, page=1, page_size=10):
        data = {'page': page, 'page_size': page_size}
        headers = {'token': self.token}
        return pe_api(
            "http://localhost:%s/jmeter/app/order/list" % PORT, headers=headers, data=data)


if __name__ == '__main__':
    unittest.main()
