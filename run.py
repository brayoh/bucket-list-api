import os
import logging.config

from app import create_app


environment = os.getenv('ENV')
app = create_app(environment)

if environment == 'testing':
    LOG_LEVEL = logging.ERROR
else:
    LOG_LEVEL = logging.INFO

# configure log formatting
logging.config.dictConfig(dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'f': {
            'format': '%(asctime)s - %(process)d - %(name)s:%(lineno)d - \
                        %(levelname)-8s - %(message)s'}},
    handlers={
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': LOG_LEVEL,
        }
    },
    root={
        'handlers': ['h'],
        'level': LOG_LEVEL,
    },
))


if __name__ == '__main__':
    app.run()
