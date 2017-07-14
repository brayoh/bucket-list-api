import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """app wide configuration settings"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class DevelopmentConfig(Config):
    """Dev config settings"""
    DEBUG = True


class TestingConfig(Config):
    """Testing config settings """
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir,
                                                           'bucketlist.db'))
    DEBUG = True


class StagingConfig(Config):
    """Staging config """
    DEBUG = True


class ProductionConfig(Config):
    """ Production config """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}