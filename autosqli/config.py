#-*-coding:utf-8-*-
class Config:

    SECRET_KEY = '142-836-543'


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    sqlmap_server = '127.0.0.1'
    sqlmap_port = "8775"
    admin_token = '2193a9c30aff56fdc1fb54b912938479'
    DATABASES = {
            'HOST': 'localhost',
            'PORT': 3306,
            'USER': 'root',
            'PWD': 'root',
            'DBNAME': 'dbtest'
    }
    db_url = "mysql+mysqlconnector://root:root@localhost/dbtest?charset=utf8"
class ProductionConfig(Config):
    DEBUG = False
    ENV = 'development'
    sqlmap_server = '127.0.0.1'
    sqlmap_port = "8775"
    admin_token = '39e382aa636cb29c3bbf1c58d9eef6e4'
    DATABASES = {
            'HOST': 'localhost',
            'PORT': 3306,
            'USER': 'root',
            'PWD': '123456',
            'DBNAME': 'db_atp'
    }
    db_url = "mysql+mysqlconnector://root:root@localhost/dbtest?charset=utf8"

Conf = DevelopmentConfig