import hashlib
import jwt
from time import time
import random
import string

SALT = 'pe'


def md5_text(text: str):
    return hashlib.md5(bytes(text, encoding='utf-8')).hexdigest()


def get_token(username):
    """get token. """
    global SALT
    headers = {"alg": "HS256"}
    payload = {"username": username, 'exp': time()+(3600*24*30)}
    token = jwt.encode(payload=payload, key=SALT,
                       algorithm='HS256', headers=headers).decode('utf-8')
    return token


def sync_token(token):
    global SALT
    return jwt.decode(token, SALT, True, algorithm='HS256')

def ranstr(num=32):
    return ''.join(random.sample(string.ascii_letters + string.digits, num))

if "__main__" == __name__:
    token = get_token('13814177763')
    print(token)
    print(sync_token(token))
