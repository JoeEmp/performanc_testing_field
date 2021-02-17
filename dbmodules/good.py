from sqlalchemy import Column, Integer, String, DateTime, Table, text
from sqlalchemy.ext.declarative import declarative_base
import datetime
from com.pe_database import ENGINE, Base, metadata, MyTable


class Good(Base):
    pass
#     __tablename__ = "pe_good"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(64), nullable=True)
#     inventory = Column(Integer, default=0)
#     price = Column(Integer, default=0)
#     create_time = Column(DateTime, default=datetime.datetime.utcnow)
#     update_time = Column(DateTime, default=datetime.datetime.utcnow)

#     def __init__(self, name, inventory=0, price=0):
#         self.name = name
#         self.inventory = inventory
#         self.price = price
#         self.create_time = datetime.datetime.utcnow()
#         self.update_time = datetime.datetime.utcnow()

#     def __str__(self):
#         return "商品名称={},库存={},价格={}".format(self.name, self.inventory, self.price)


GoodTable = Table(
    'pe_good',
    metadata,
    Column('id', Integer, primary_key=True),
    Column("name", String(64), nullable=False),
    Column("inventory", Integer, server_default=text('0')),
    Column('price', Integer, server_default=text('0'),comment='单位为分'),
    Column('create_time', DateTime,
           server_default=text('CURRENT_TIMESTAMP')),
    Column('update_time', DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
)
