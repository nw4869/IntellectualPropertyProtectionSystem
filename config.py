# coding=utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

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

    @staticmethod
    def init_app(app):
        # init flask debug toolbar
        if DevelopmentConfig.DEBUG:
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
