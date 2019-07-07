import os

basedir = os.path.abspath(os.path.dirname(__file__))

API_KEY = '886281758:AAGNFb-lIddVLB4n7KEkRMCptNeV5mJnufU'

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')