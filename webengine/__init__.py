from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import AppConfig

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=AppConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from webengine.apis.routes import apis
    from webengine.main.routes import main
    from webengine.news.routes import news
    from webengine.users.routes import users
    from webengine.misc.routes import misc

    app.register_blueprint(apis)
    app.register_blueprint(main)
    app.register_blueprint(news)
    app.register_blueprint(users)
    app.register_blueprint(misc)

    return app
