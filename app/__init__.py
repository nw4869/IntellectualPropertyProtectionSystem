from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_login import LoginManager
from flask_uploads import configure_uploads, patch_request_class, UploadSet
from flask_moment import Moment
import logging
from logging import handlers

from web3 import Web3, KeepAliveRPCProvider, contract

from config import config
from app import custom_error_pages

bootstrap = Bootstrap()
db = SQLAlchemy()
babel = Babel()
login_manager = LoginManager()
moment = Moment()

# upload_photos = None
upload_files = None

web3 = Web3(KeepAliveRPCProvider())
MyContract = None
my_contract = None

from app.models import *


def create_app(config_name):
    app = Flask(__name__)
    the_config = config[config_name]
    app.config.from_object(the_config)
    the_config.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    babel.init_app(app)
    moment.init_app(app)

    # config flask-login
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warn'
    login_manager.login_message = '请先登录'

    # logging
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(log_formatter)
    app.logger.addHandler(handler)

    # config flask-uploads
    # global upload_photos
    # upload_photos = UploadSet('photos', the_config.FILE_TYPE_IMAGES)
    global upload_files
    upload_files = UploadSet('files', the_config.FILE_TYPE_ALLOW)
    configure_uploads(app, upload_files)

    # construct ethereum contract
    contract_data = the_config.contract_data
    global MyContract
    MyContract = contract.Contract.factory(web3, contract_name='MyContract', **contract_data)
    global my_contract
    my_contract = MyContract(address=contract_data['address'])

    with app.app_context():
        db.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .showcase import showcase as showcase_blueprint
    app.register_blueprint(showcase_blueprint, url_prefix='/showcase')

    from .etheruem import ethereum
    app.register_blueprint(ethereum, url_prefix='/ethereum')

    app.register_error_handler(403, custom_error_pages.forbidden)
    # app.error_handler_spec[None][404] = custom_error_pages.page_not_found
    app.register_error_handler(404, custom_error_pages.page_not_found)
    # app.error_handler_spec[None][500] = custom_error_pages.internal_server_error
    app.register_error_handler(500, custom_error_pages.internal_server_error)

    print('app created')

    return app
