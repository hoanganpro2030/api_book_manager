# coding=utf-8
import logging

import sqlalchemy as _sa
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from flask_restplus import fields, Model
from base_task.models import db


__author__ = 'Kien'
_logger = logging.getLogger('api')


class TimestampMixin(object):
    """
    Adds `created_at` and `updated_at` common columns to a derived
    declarative model.
    """

    @declared_attr
    def created_at(self):
        return _sa.Column(_sa.TIMESTAMP,
                          server_default=func.now(), default=func.now(),
                          nullable=False)

    @declared_attr
    def updated_at(self):
        return _sa.Column(_sa.TIMESTAMP, server_default=func.now(),
                          default=func.now(),
                          nullable=False, onupdate=func.now())


class ErrorSchema:
    """
    Add error marshal swagger for error return
    """
    error_res = {
        'code': fields.String(required=True, description='Error code'),
        'message': fields.String(required=True, description='Error message'),
        'success': fields.String(description='Error message'),
        'data': fields.Raw(description='Error data')
    }


class ResponseModel:
    """
    Add success model use in marshal_with for success return
    """

    success_response = Model('success_response', {
        'code': fields.String(required=True),
        'message': fields.String(),
        'result': fields.Raw(),
    })

    error_response = Model('error_response', {
        'code': fields.String(required=True, description='error code'),
        'message': fields.String(required=True, description='error message'),
        'extra': fields.Raw(),
    })
