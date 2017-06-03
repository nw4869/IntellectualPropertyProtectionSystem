# coding=utf-8
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

    # config for upload file
    UPLOADS_DEFAULT_DEST = basedir

    MAX_CONTENT_LENGTH = 64 * 1024 * 1024   # 64 MB upload file max length

    FILE_TYPE_TEXT = ('txt',)
    FILE_TYPE_DOCUMENTS = tuple('rtf odf ods gnumeric abw doc docx xls xlsx'.split())
    FILE_TYPE_IMAGES = tuple('jpg jpe jpeg png gif svg bmp'.split())
    FILE_TYPE_AUDIO = tuple('wav mp3 aac ogg oga flac'.split())
    FILE_TYPE_DATA = tuple('csv ini json plist xml yaml yml'.split())
    FILE_TYPE_SCRIPTS = tuple('js php pl py rb sh'.split())
    FILE_TYPE_ARCHIVES = tuple('gz bz2 zip tar tgz txz 7z'.split())
    FILE_TYPE_EXECUTABLES = tuple('so exe dll'.split())
    # FILE_TYPE_ALLOW = FILE_TYPE_TEXT + FILE_TYPE_DOCUMENTS + FILE_TYPE_DATA + FILE_TYPE_ARCHIVES + FILE_TYPE_IMAGES
    FILE_TYPE_ALLOW = ('jpg',)

    # ethereum
    CONFIRM_BLOCK_NUM = 3
    contract_conf_path = os.path.join(basedir, 'contract.json')
    try:
        with open(contract_conf_path) as f:
            contract_data = json.load(f)
        assert contract_data.get('abi')
        assert any((contract_data.get('bytecode'), contract_data.get('address')))
    except:
        raise Exception('failed to load contract config from "contract.json"!')

    @staticmethod
    def update_contract_config(contract_data):
        with open(Config.contract_conf_path, 'w') as f:
            json.dump(contract_data, f, indent=4, sort_keys=True)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                           'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:4869@localhost/property_system_dev?charset=utf8'

    # 加载bootstrap本地css与js文件
    BOOTSTRAP_SERVE_LOCAL = True

    ENABLE_DEBUG_TOOLBAR = False

    @staticmethod
    def init_app(app):
        # init flask debug toolbar
        if DevelopmentConfig.DEBUG and DevelopmentConfig.ENABLE_DEBUG_TOOLBAR:
            try:
                from flask_debugtoolbar import DebugToolbarExtension
                app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
                DebugToolbarExtension(app)
            except:
                print("pass... flask_debugtoolbar not install")


class TestingConfig(Config):
    SERVER_NAME = 'localhost:5000'
    TESTING = True
    WTF_CSRF_ENABLED = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #                           'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:4869@localhost/property_system_test?charset=utf8'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
    # 'default': ProductionConfig
}


def get_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']