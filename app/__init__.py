from flask import Flask
from flask.ext.redis import FlaskRedis
#from config import config

redis_store = FlaskRedis()

def create_app(config_name):
    app = Flask(__name__)
    #app.config.from_object(config[config_name])

    redis_store.init_app(app)

    from .orgs import orgs as orgs_blueprint
    app.register_blueprint(orgs_blueprint)

    from .indv import indv as indv_blueprint
    app.register_blueprint(indv_blueprint,url_prefix='/indv')

    return app
