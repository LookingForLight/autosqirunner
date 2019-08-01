#-*-coding:utf-8-*-
class Config:

    SECRET_KEY = '142-836-543'


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    sqlmap_server = '127.0.0.1'
    sqlmap_port = "8775"
    admin_token = 'cfd0502933c252f213d2189cace9f924'

class ProductionConfig(Config):
    DEBUG = False


Conf = DevelopmentConfig