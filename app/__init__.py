from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    login.init_app(app)
    login.login_view = 'authentication.login'
    login.login_message_category = 'warning'

    
    with app.app_context():
        from app.blueprints.blog import bp as blog
        app.register_blueprint(blog)
        
        from app.blueprints.api import bp as api
        app.register_blueprint(api)

        from app.blueprints.shop import bp as shop
        app.register_blueprint(shop)

        from app.blueprints.main import bp as main
        app.register_blueprint(main)

        from app.blueprints.authentication import bp as authentication
        app.register_blueprint(authentication)
        
        from .import routes, models
    return app
