import unittest
import os
import logging
from dbmodules.base import BaseDBServer, CoreDBServer
from dbmodules.good import Good, GoodTable
from dbmodules.user import Users, UserTable
from dbmodules.order import Order, OrderTable
from faker import Faker
from com.pe_encrypt import md5_text
from faker.providers import BaseProvider
from random import choice, seed
import pymysql
from settings import *
from com.pe_database import metadata, ENGINE

root_dir = os.path.abspath(os.path.dirname(__file__))
log_file = os.path.join(root_dir, 'env_init.log')
user_data_file = os.path.join(root_dir, './tests/user.txt')
good_data_file = os.path.join(root_dir, './tests/good.txt')
db_file = os.path.join(root_dir, "petest.db")
seed(0)
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(message)s',
                    filename=log_file
                    )


class GoodProvider(BaseProvider):
    tags = ['', '低过老罗', '工厂价', '全网最低', ]
    names = ['肯尼亚AA水洗', '耶加雪菲水洗', '智能水壶', '小米手机', 'iPhone',
             '星际争霸2数字典藏版', '飞鹤奶粉', 'MacbookAir M1', '蜜桃猫手机壳'
             '星空', '蒙娜丽莎', '伏尔加河上的纤夫', '马拉之死', '这个需求做不了']
    age = ['2020款', '2021款', '2022款', '']

    def good_name(self):
        good = choice(self.age)+" "+choice(self.names) + " "+choice(self.tags)
        return good.strip(' ')


def create_schema():
    try:
        db = pymysql.connect("localhost", "root", "123456")
        db.cursor().execute("CREATE SCHEMA `%s` DEFAULT CHARACTER SET utf8mb4 ;" % MYSQL_SCHEMA)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()


def set_time_zone():
    # 修正时区
    try:
        db = pymysql.connect("localhost", "root", "123456")
        db.cursor().execute("set global time_zone = '+8:00';")
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()


class create_db_testcase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_schema()
        set_time_zone()

    def setUp(self):
        suffix = self._testMethodName.split('_')[-2]
        if 'user' == suffix.lower():
            self.table = UserTable
        elif 'good' == suffix.lower():
            self.table = GoodTable
        elif 'order' == suffix.lower():
            self.table = OrderTable
        self.table.drop(ENGINE, checkfirst=True)
        self.table.create(ENGINE, checkfirst=True)
        self.db = CoreDBServer(self.table)

    # @unittest.skip('skip')
    def test_create_user_table(self):
        values = {"username": 'test_user', "password": '123564'}
        self.db.insert(**values)

    # @unittest.skip('skip')
    def test_create_good_table(self):
        values = {'name': 'test_good'}
        self.db.insert(**values)

    # @unittest.skip('skip')
    def test_create_order_table(self):
        values = {'username': 'lilei',
                  'order_no': '202001250159591234', 'good_ids': '[1,2]'}
        self.db.insert(**values)

    def tearDown(self):
        self.db.clear()
        return super().tearDown()

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()


class init_faker_data():

    def __init__(self):
        self.fake = Faker('zh-CN')
        self.fake.add_provider(GoodProvider)
        Faker.seed(0)

    def add_user_data(self):
        self.table = CoreDBServer(UserTable)
        data_list = []
        with open(user_data_file, 'w') as f:
            name_set = set([])
            for _ in range(10000):
                while True:
                    cur_len = len(name_set)
                    username, password = self.fake.email(), self.fake.password()
                    name_set.add(username)
                    if len(name_set) > cur_len:
                        break
                data_list.append(
                    {"username": username, "password": md5_text(password)
                     }
                )
                f.write(username+','+password+os.linesep)
        self.table.many_insert(data_list=data_list)

    def add_good_data(self):
        self.table = CoreDBServer(GoodTable)
        data_list = []
        with open(good_data_file, 'w') as f:
            for _ in range(1000):
                godd_name, inventory, price = self.fake.good_name(
                ), self.fake.pyint(), self.fake.pyint()
                data_list.append(
                    {"name": godd_name, "inventory": inventory, "price": price})
                f.write(godd_name+","+str(inventory) +
                        ","+str(price)+os.linesep)
        self.table.many_insert(data_list=data_list)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        unittest.main()
    elif 'data' == sys.argv[1]:
        data = init_faker_data()
        data.add_user_data()
        data.add_good_data()
