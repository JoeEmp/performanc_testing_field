from sqlalchemy import create_engine, event, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


class Base():
    pass


def pymysql_patch():
    # 这里作恶一下
    # 已知我们使用的是pymysql,我们修改一下默认游标为字典游标.
    # Connection.cursor(cursor: Type[Cursor])
    # Create a new cursor to execute queries with.
    # :param cursor: The type of cursor to create; 
    # one of Cursor, SSCursor, DictCursor, or SSDictCursor. None means use Cursor.
    from pymysql.cursors import Cursor, DictCursor
    Cursor = DictCursor


ENGINE = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/pe_test?charset=utf8mb4",
    echo=False, isolation_level="READ UNCOMMITTED")
metadata = MetaData()
pymysql_patch()


class MyTable():
    def __init__(self):
        self.table = None

    def create(self):
        self.table.create(ENGINE, checkfirst=True)

    @property
    def name(self):
        return self.table.name

    def insert(self, *args, **kwargs):
        return self.table.insert()
