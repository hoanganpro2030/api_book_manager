# coding=utf-8
import logging
import redis
import flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from base_task import admin


__author__ = 'SonLp'
_logger = logging.getLogger('api')

SENTRY_DSN = 'SENTRY_DSN'


def create_app():
    import config
    import logging.config
    import os

    from . import api, models
    from base_task import helpers

    def load_app_config(app):
        """
        Load app's configurations
        :param flask.Flask app:
        :return:
        """
        app.config.from_object(config)
        app.config.from_pyfile('config.py', silent=True)

    app = flask.Flask(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.join(config.ROOT_DIR, 'instance')
    )
    app.json_encoder = helpers.JSONEncoder
    load_app_config(app)

    # Register new flask project here and get new dsn: https://sentry.io
    dns = SENTRY_DSN if os.environ.get('SEND_REPORT') == 'true' else None

    app.config['RESTPLUS_MASK_SWAGGER'] = False

    sentry_sdk.init(
        dsn=dns,
        integrations=[FlaskIntegration()],
        environment=app.config['ENV_MODE'],
        in_app_exclude=['app.extensions.exceptions'],
    )

    # Add redis provider

    _logger.info("REDIS_ENABLED={0}".format(os.environ.get('REDIS_ENABLED')))

    if os.environ.get('REDIS_ENABLED'):
        _logger.info("Init Redis cache....")

        app.config['REDIS_PROVIDER'] = redis.Redis(host=app.config['REDIS_HOST'],
                                               port=app.config['REDIS_PORT'])

    # setup logging
    logging.config.fileConfig(app.config['LOGGING_CONFIG_FILE'],
                              disable_existing_loggers=False)
    app.secret_key = config.FLASK_APP_SECRET_KEY
    models.init_app(app)
    api.init_app(app)
    admin.init_app(app)
    return app


app = create_app()
