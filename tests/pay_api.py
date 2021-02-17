import unittest
import sys
import os
from time import sleep
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.sep.join(root_dir.split(os.sep)[:-1]))


class pay_api(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = login()['token']
        return super().setUpClass()

    # @unittest.skip('skip')
    def test_pay_exp_order(self):
        """支付过期订单."""
        good_ids = '[2]'
        order_no = order_api().order_add(good_ids)['order_no']
        # 操作库过期订单
        exp_order(order_no)
        ret = self.pay_order(order_no)
        self.assertIsInstance(ret, dict, ret)
        self.assertIn('过期', ret['msg'], ret)

    def test_pay_order(self):
        """支付订单"""
        good_ids = '[2]'
        order_no = order_api().order_add(good_ids)['order_no']
        ret = self.pay_order(order_no)
        self.assertEqual(0, ret['code'], ret)

    def test_pay_paid_order(self):
        """支付已支付订单"""
        good_ids = '[2]'
        order_no = order_api().order_add(good_ids)['order_no']
        ret = self.pay_order(order_no)
        ret = self.pay_order(order_no)
        self.assertIn('重复支付', ret['msg'], ret)

    def test_pay_not_exist_order(self):
        order_no = '2123'
        ret = self.pay_order(order_no)
        self.assertIn('订单不存在', ret['msg'], ret)

    def pay_order(self, order_no):
        data = {'order_no': order_no}
        headers = {'token': self.token}
        return pe_api("http://localhost:%s/jmeter/pay" % PORT, data=data, headers=headers)


if __name__ == '__main__':
    from order_api import order_api
    from con_api import login, requests, exp_order, pe_api
    from settings import PORT
    unittest.main()
