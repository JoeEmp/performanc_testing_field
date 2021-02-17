import logging


logging.basicConfig(
    # format="%(asctime)s",
    format="%(asctime)s %(levelname)s \"%(pathname)s\", line %(lineno)d, %(message)s",
    level=logging.INFO,
    # filename='server.log'
)

PORT = 10086

MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PWD = '123456'
MYSQL_SCHEMA = 'pe_test'
