import unittest
import sys
import os
from time import sleep
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.sep.join(root_dir.split(os.sep)[:-1]))
from con_api import login, requests, exp_order, pe_api
from settings import PORT

class order_api(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = login()['token']
        return super().setUpClass()

    def test_order_detail(self):
        """商品详情"""
        good_id = self.good_list()['list'][0]['id']
        ret = self.good_detail(good_id)
        self.assertIn('good', ret.keys(), ret)

    def test_not_exist_good_detail(self):
        good_id = '0'
        ret = self.good_detail(good_id)
        self.assertIn('商品不存在', ret['msg'], ret)

    def test_good_list(self):
        """商品列表"""
        ret = self.good_list()
        self.assertIn('list', ret.keys(), ret)

    def test_sort_by_inventory(self):
        """按库存排序. """
        sorts_by = "[['inventory', '0']]"
        l = self.good_list(page_size=10, sorts_by=sorts_by)['list']
        good1, good2 = l[0]['inventory'], l[1]['inventory']
        self.assertLess(good1, good2, l[:2])

    def good_detail(self, good_id):
        data = {"id": good_id}
        return pe_api(
            "http://localhost:%s/jmeter/app/good/detail" % PORT, data=data)

    def good_list(self, page=1, page_size=10, sorts_by=[]):
        data = {'page': str(page), 'page_size': str(page_size), "sorts_by": sorts_by}
        return pe_api(
            "http://localhost:%s/jmeter/app/good/list" % PORT, data=data)


if __name__ == '__main__':
    unittest.main()
