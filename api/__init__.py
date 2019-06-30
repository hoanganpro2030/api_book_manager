# coding=utf-8
import logging

from flask import Blueprint

from ..models import db

from flask_restplus import Api, Resource, fields
# Import all necesary API NameSpace here

from base_task.api.books import api as books_api

from base_task.api.authors import api as authors_api


__author__ = 'ThucNC'
_logger = logging.getLogger('api')


api_wms = Blueprint('api', __name__, url_prefix='/api')

custom_definition = {
    'info': {
        'x-logo': {
            'url': 'https://teko-vn.github.io/api-docs/Teko-Logo-01.svg'
        }
    },
}

api = Api(
    app=api_wms,
    version='1.0',
    title='Teko Book Manager API',
    validate=False,
    description='This documentation describes APIs used in/exposed from Teko micro-services ecosystem \
    # Introduction\
    These specifications are following\
    [OpenAPI 3.0.0 format](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md).',
    license='Apache 2.0',
    license_url='http://www.apache.org/licenses/LICENSE-2.0.html',
    contact_email='son.lp@teko.vn'
    # doc='' # disable Swagger UI
)


# add custom definition

def init_app(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    api.add_namespace(authors_api)
    api.add_namespace(books_api)

    app.register_blueprint(api_wms)
