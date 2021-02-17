import unittest
import sys
import os
from time import sleep
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.sep.join(root_dir.split(os.sep)[:-1]))
from con_api import requests, pe_api, CoreDBServer, UserTable
from settings import PORT

class login_api(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        row = CoreDBServer(UserTable).select().first()
        cls.username = row['username']
        cls.password = row['password']
        return super().setUpClass()

    def test_login(self):
        ret = self.login(self.username, self.password)
        self.assertIn('token', ret.keys())

    def test_legal_user(self):
        ret = self.login(self.username+"123", self.password)
        self.assertIn('不存在', ret['msg'])

    def test_error_password(self):
        ret = self.login(self.username, self.password+'213')
        self.assertIn('错误', ret['msg'])

    def login(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        return pe_api('http://localhost:%s/jmeter/login' % PORT, data=data)

if __name__ == '__main__':
    unittest.main()