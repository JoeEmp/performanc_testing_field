from sqlalchemy import Column, Integer, String, DateTime, Table, text
from sqlalchemy.ext.declarative import declarative_base
import datetime
from com.pe_database import ENGINE, Base, metadata, MyTable


class Users(Base):
    pass
    # __tablename__ = "pe_user"

    # id = Column(Integer, primary_key=True)
    # username = Column(String(64), nullable=True, unique=True)
    # password = Column(String(64), nullable=True)
    # money = Column(Integer, default=0)
    # create_time = Column(DateTime, default=datetime.datetime.now)
    # update_time = Column(DateTime, default=datetime.datetime.now)

    # def __init__(self, username, password, money=0):
    #     self.username = username
    #     self.password = password
    #     self.money = money
    #     self.create_time = datetime.datetime.now
    #     self.update_time = datetime.datetime.now

    # def __str__(self):
    #     return "username={},money={}".format(self.username, self.money)


UserTable = Table(
    'pe_user', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('password', String(64), nullable=False),
    Column("money", Integer, server_default=text('0')),
    Column('create_time', DateTime,
           server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
)
