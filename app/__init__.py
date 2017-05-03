from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_login import LoginManager


from config import config
from . import custom_error_pages

bootstrap = Bootstrap()
db = SQLAlchemy()
babel = Babel()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # app.error_handler_spec[None][404] = custom_error_pages.page_not_found
    app.register_error_handler(404, custom_error_pages.page_not_found)
    # app.error_handler_spec[None][500] = custom_error_pages.internal_server_error
    app.register_error_handler(500, custom_error_pages.internal_server_error)

    print('app created')

    return app
