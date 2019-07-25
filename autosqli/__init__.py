#-*-coding:utf-8-*-

from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Conf
from .main import sqil as sqli_bluepoint
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Conf)
    bootstrap.init_app(app)

    # app.jinja_env.variable_start_string = '[['  #修改jinja转义符
    # app.jinja_env.variable_end_string = ']]'
    app.register_blueprint(sqli_bluepoint,url_prefix = '/autosqli')
    if Conf.DEBUG == True:
        app.run(host='0.0.0.0')

    else:
        app.run(host='10.101.52.94', port=5004)
    return app

