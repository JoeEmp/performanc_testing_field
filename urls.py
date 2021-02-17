from handlers.hello import *
from handlers.about import *
from handlers.login import *
from handlers.pay import *
from handlers.order import *
from handlers.good import *


url_patterns = [
    (r'/jmeter/login', LoginHandler),
    (r'/jmeter/pay', PayHandler),
    (r"/", HelloHandler),
    (r"/about", AboutHandler),
    (r"/jmeter/app/order/.+?", OrderHandler),
    (r"/jmeter/app/good/.+?", GoodHandler)
]
