from ..models import db

from flask_restplus import Api, Resource, fields, Namespace, abort

from base_task.admin.models import Authors

from ..api import custom_fields

from werkzeug.exceptions import BadRequest

import datetime

api = Namespace('Authors', description='Authors operations')

authors = api.model('Authors', {
        'id': fields.Integer(readOnly=True, description='The task unique identifier', example=1),
        'first_name': fields.String(required=True, description='The first name of author', example='dang',
                                    min_length=1, max_length=100),
        'last_name': fields.String(required=True, description='The last name of author', example='hoang an',
                                   min_length=1, max_length=100),
        'email': custom_fields.Email(required=True, description='The email of author', example='hoangan@gmail.com'),
        'phone': custom_fields.Phone(required=True, description='The phone number of author', example='0986797221',
                                     min_length=10, max_length=10),
        'address': fields.String(required=True, description='The address of author', example='Nha Trang',
                                 max_length=150),
        'status': fields.Boolean(description='The status of author'),
        'created': fields.DateTime(dt_format='rfc822', description='date created'),
        'updated': fields.DateTime(dt_format='rfc822', description='date updated'),
})


authors_put = api.model('Authorsput', {
        'id': fields.Integer(readOnly=True, description='The task unique identifier', example=1),
        'first_name': fields.String(description='The first name of author', example='dang',
                                    min_length=1, max_length=100),
        'last_name': fields.String(description='The last name of author', example='hoang an',
                                   min_length=1, max_length=100),
        'email': custom_fields.Email(description='The email of author', example='hoangan@gmail.com'),
        'phone': custom_fields.Phone(description='The phone number of author', example='0986797221',
                                     min_length=10, max_length=10),
        'address': fields.String(description='The address of author', example='Nha Trang',
                                 max_length=150),
        'status': fields.Boolean(description='The status of author'),
        'created': fields.DateTime(dt_format='rfc822', description='date created'),
        'updated': fields.DateTime(dt_format='rfc822', description='date updated'),
})


@api.route('/')
class TodoAuthorList(Resource):
    '''Shows a list of all Authors, and lets you POST to add new authors'''

    @api.doc('get_author_list')
    @api.marshal_list_with(authors, envelope='resource')
    def get(self):
        '''List all books'''
        return Authors.query.all(), 200

    @api.doc('create_author')
    @api.expect(authors, validate=True)
    @api.marshal_list_with(authors, code=201)
    @api.response(400, "Bad request")
    def post(self):
        '''Add new author'''
        validate_payload(api.payload, authors)
        vemail = Authors.query.filter_by(email=api.payload['email']).first()
        if vemail is not None:
            abort(400, 'Email have already existed')
        vphone = Authors.query.filter_by(phone=api.payload['phone']).first()
        if vphone is not None:
            abort(400, 'Phone have already existed')
        author = Authors(first_name=api.payload['first_name'],
                         last_name=api.payload['last_name'],
                         email=api.payload['email'],
                         phone=api.payload['phone'],
                         address=api.payload['address'])
        author.created = datetime.datetime.now()
        author.updated = datetime.datetime.now()
        db.session.add(author)
        db.session.commit()
        return author, 201


@api.route('/<int:id>')
@api.response(404, 'Todo not found')
@api.param('id', 'The task identifier')
class TodoAuthor(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''

    @api.doc('get_author_by_id')
    @api.marshal_list_with(authors)
    def get(self, id):
        '''Get Author'''
        a = Authors.query.filter_by(id=id).first()
        if a is not None:
            return a, 200
        else:
            api.abort(404)

    @api.doc('delete_author_by_id')
    @api.response(204, 'Delete Successfully')
    def delete(self, id):
        '''Delete Author'''
        a = Authors.query.filter_by(id=id).first()
        if a is not None:
            db.session.delete(a)
            db.session.commit()
            return {'message': 'Delete successfully'}, 204
        else:
            api.abort(404, 'Not found')

    @api.doc('update_author_by_id')
    @api.expect(authors_put, validate=True)
    @api.marshal_with(authors, skip_none=True, code=201)
    @api.response(400, 'Bad request')
    def put(self, id):
        '''Update Author'''
        validate_payload(api.payload, authors_put)
        a = Authors.query.filter_by(id=id).first()
        if a is not None:
            for x in api.payload:
                if x == 'first_name':
                    a.first_name = api.payload['first_name']
                    continue
                if x == 'last_name':
                    a.last_name = api.payload['last_name']
                    continue
                if x == 'status':
                    a.status = api.payload['status']
                    continue
                if x == 'address':
                    a.address = api.payload['address']
                    continue
                if x == 'phone':
                    vphone = Authors.query.filter_by(phone=api.payload['phone']).first()
                    if vphone is not None and vphone.id != id:
                        abort(400, "Invalid, Phone number already existed")
                    a.phone = api.payload['phone']
                if x == 'email':
                    vemail = Authors.query.filter_by(email=api.payload['email']).first()
                    if vemail is not None and vemail.id != id:
                        abort(400, "Invalid, Email already existed")
                    a.email = api.payload['email']

            a.updated = datetime.datetime.now()
            db.session.commit()
            return a, 201
        else:
            api.abort(404, "Not found")


def validate_payload(payload, api_model):
    # check if any reqd fields are missing in payload
    for key in api_model:
        if api_model[key].required and key not in payload:
            e = BadRequest('My custom message')
            e.data = {'custom': 'Required field \'%s\' missing' % key}
            raise e
    # check payload
    for key in payload:
        field = api_model[key]
        if isinstance(field, fields.List):
            field = field.container
            data = payload[key]
        else:
            data = [payload[key]]
        if isinstance(field, custom_fields.CustomField) and hasattr(field, 'validate'):
            for i in data:
                if not field.validate(i):
                    e = BadRequest('My custom message')
                    e.data = {'custom': 'Validation of \'%s\' field failed' % key}
                    raise e