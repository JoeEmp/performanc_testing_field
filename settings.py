import logging
import sys

if len(sys.argv) >= 2 and sys.argv[1] == 'debug':
    env = 'debug'
else:
    env = 'pro'

log_config = {
    'debug': dict(
        format="%(asctime)s %(levelname)s \"%(pathname)s\", line %(lineno)d, %(message)s",
        level=logging.INFO,
    ),
    'pro': dict(
        format="%(asctime)s %(levelname)s \"%(pathname)s\", line %(lineno)d, %(message)s",
        level=logging.WARNING,
        filename='server.log'
    )
}

logging.basicConfig(
    **log_config[env]
)

PORT = 10086

MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PWD = '123456'
MYSQL_SCHEMA = 'pe_test'
