from sqlalchemy import Column, Integer, String, DateTime, Table, text
from sqlalchemy.ext.declarative import declarative_base
import datetime
from com.pe_database import ENGINE, Base, metadata, MyTable


class Order(Base):
    pass
    # __tablename__ = "pe_order"

    # id = Column(Integer, primary_key=True)
    # username = Column(String(64), nullable=True)
    # order_no = Column(String(64), nullable=True)
    # good_ids = Column(String(100), nullable=True)
    # pay_id = Column(String(64))
    # sum_price = Column(Integer, default=0)
    # status = Column(Integer, default=0)
    # create_time = Column(DateTime, nullable=True,
    #                      default=datetime.datetime.utcnow)
    # update_time = Column(DateTime,  nullable=True,
    #                      default=datetime.datetime.utcnow,
    #                      onupdate=datetime.datetime.utcnow)

    # def __init__(self, username, order_no, good_ids=[], sum_price=0):
    #     self.username = username
    #     self.order_no = order_no
    #     self.good_ids = ','.join([str(good_id) for good_id in good_ids])
    #     self.sum_price = sum_price
    #     self.status = 0
    #     self.create_time = datetime.datetime.utcnow()
    #     self.update_time = datetime.datetime.utcnow()

    # def __str__(self):
    #     return "username={},order_no={},总单价={},goods_id={}".format(
    #         self.username, self.order_no, self.sum_price, self.good_ids)


OrderTable = Table(
    "pe_order", metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=True),
    Column("order_no", String(64), nullable=True),
    Column("good_ids", String(100), nullable=True),
    Column("pay_id", String(64)),
    Column('sum_price', Integer, default=0),
    Column('status', Integer, default=0,comment='0是未支付,1是成功,2是失败,3是交易关闭'),
    Column('create_time', DateTime, server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
)
