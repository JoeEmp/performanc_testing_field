import unittest
import sys
import os
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.sep.join(root_dir.split(os.sep)[:-1]))


class test_db_module(unittest.TestCase):

    def setUpClass(cls):
        return super().setUpClass()

    def setUp(self):
        self.db = CoreDBServer(UserTable)
        return super().setUp()

    def test_select(self):
        wheres = [
            ['username', 'eq', 'nliu@yahoo.com'],
            ['id', 'eq', 2]
        ]
        row = self.db.select(wheres).first()
        self.assertEqual('nliu@yahoo.com', row['username'])

    def test_update(self):
        new_values = {'money': 0}
        wheres = [
            ['username', 'eq', 'sgong@yangzeng.cn']
        ]
        ret = self.db.update(wheres=wheres, **new_values)
        ret = self.db.select(wheres).first()
        self.assertEqual(0, ret['money'])


if "__main__" == __name__:
    from dbmodules.user import UserTable
    from dbmodules.base import CoreDBServer
    from sqlalchemy import text, event, delete, select, update
    from sqlalchemy.sql.dml import Update
    unittest.main()
