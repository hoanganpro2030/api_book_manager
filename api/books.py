from ..models import db

from flask_restplus import Api, Resource, fields, Namespace

from base_task.admin.models import Books

from ..api import custom_fields

from werkzeug.exceptions import BadRequest

import datetime

api = Namespace('Books', description='Book operations')

books = api.model('Books', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier', example=1),
    'title': fields.String(required=True, description='The title of book', example='Kieu story', max_length=100),
    'isbn': custom_fields.Isbn(required=True, description='The code isbn of book', example='978-604-0-00000-2',
                               min_length=17, max_length=17),
    'year': fields.Integer(required=True, description='The year of book', example=2017,
                           min=0, max=datetime.datetime.now().year),
    'author_id': fields.Integer(required=True, description='The author id who write the book', example=4),
    'status': fields.Boolean(description='The status of book', example=True),
    'created': fields.DateTime(dt_format='rfc822', description='date created'),
    'updated': fields.DateTime(dt_format='rfc822', description='date updated'),
    'views': fields.Integer(description='The views number of book', example=5, min=0),
    'votes': fields.Integer(description='The votes number of book', example=4, min=0),
    'downloads': fields.Integer(description='The downloads number of book', example=2, min=0),
})


books_put = api.model('Booksput', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier', example=1),
    'title': fields.String(description='The title of book', example='Kieu story', max_length=100),
    'isbn': custom_fields.Isbn(description='The code isbn of book', example='978-604-0-00000-2',
                               min_length=17, max_length=17),
    'year': fields.Integer(description='The year of book', example=2017,
                           min=0, max=datetime.datetime.now().year),
    'author_id': fields.Integer(description='The author id who write the book', example=4),
    'status': fields.Boolean(description='The status of book', example=True),
    'created': fields.DateTime(dt_format='rfc822', description='date created'),
    'updated': fields.DateTime(dt_format='rfc822', description='date updated'),
    'views': fields.Integer(description='The views number of book', example=5, min=0),
    'votes': fields.Integer(description='The votes number of book', example=4, min=0),
    'downloads': fields.Integer(description='The downloads number of book', example=2, min=0),
})


@api.route('/')
class TodoBooklList(Resource):
    '''Shows a list of all books, and lets you POST to add new books'''

    @api.doc('get_books_list')
    @api.marshal_list_with(books)
    def get(self):
        '''List all books'''
        b = Books.query.all()
        return b, 200

    @api.doc('create_books')
    @api.expect(books, validate=True)
    @api.response(400, "Bad request")
    @api.marshal_list_with(books, code=201)
    def post(self):
        '''Create a new book'''
        validate_payload(api.payload, books)
        visbn = Books.query.filter_by(isbn=api.payload['isbn']).first()
        if visbn is not None:
            api.abort(400, "Invalid, ISBN already existed")

        b = Books(title=api.payload['title'], isbn=api.payload['isbn'], year=api.payload['year'],
                  author_id=api.payload['author_id'])
        b.updated = datetime.datetime.now()
        b.created = datetime.datetime.now()
        db.session.add(b)
        db.session.commit()
        return b, 201


@api.route('/<int:id>')
@api.response(404, 'Todo not found')
@api.param('id', 'The task identifier')
class TodoBook(Resource):
    '''Shows a book by id, and lets you POST, PUT, DELETE book'''

    @api.doc('get_book_by_id')
    @api.marshal_list_with(books)
    def get(self, id):
        '''Get a Book'''
        a = Books.query.filter_by(id=id).first()
        if a is not None:
            return a, 200
        else:
            api.abort(404)

    @api.doc('update_book_by_id')
    @api.expect(books_put, validate=True)
    @api.response(400, 'Bad request')
    @api.marshal_with(books, code=201)
    def put(self, id):
        '''Update a Book'''
        # validate
        validate_payload(api.payload, books_put)
        b = Books.query.filter_by(id=id).first()

        # Check field exists to update
        if b is not None:
            for x in api.payload:
                if x == 'title':
                    b.title = api.payload['title']
                if x == 'isbn':
                    visbn = Books.query.filter_by(isbn=api.payload['isbn']).first()
                    if visbn is not None and visbn.id != id:
                        api.abort(400, "Invalid, ISBN already existed")
                    b.isbn = api.payload['isbn']
                if x == 'year':
                    b.year = api.payload['year']
                if x == 'status':
                    b.status = api.payload['status']
                if x == 'views':
                    b.views = api.payload['views']
                if x == 'downloads':
                    b.downloads = api.payload['downloads']
                if x == 'votes':
                    b.votes = api.payload['votes']
            b.updated = datetime.datetime.now()
            db.session.commit()
            return b, 201
        else:
            api.abort(404)

    @api.doc('delete_book_by_id')
    @api.response(204, 'Delete successfully')
    def delete(self, id):
        '''Delete a Book'''
        b = Books.query.filter_by(id=id).first()
        if b is not None:
            db.session.delete(b)
            db.session.commit()
            return {'message': 'Delete successfully'}, 204
        else:
            api.abort(404)


search_title = api.model('s_title', {
    'title': fields.String(required=True, description='The key word to search', max_length=100)
})


search_isbn = api.model('s_isbn', {
    'isbn': custom_fields.Isbn(required=True, description='The key word to search', max_length=17, min_length=17)
})



@api.route('/search/list')
class SearchByTitle(Resource):
    '''Search book by title'''
    @api.doc('search_by_title')
    @api.expect(search_title, validate=True)
    @api.response(400, 'Bad Request')
    @api.marshal_list_with(books, code=200)
    def post(self):
        b = Books.query.filter(Books.title.like("%"+str(api.payload['title'])+"%")).all()
        return b, 200


@api.route('/search/one')
class SearchByIsbn(Resource):
    '''Search book by isbn'''
    @api.doc('search_by_isbn')
    @api.marshal_with(books, code=200)
    @api.expect(search_isbn, validate=True)
    @api.response(404, 'Book not found')
    @api.response(400, 'Bad request')
    def post(self):
        validate_payload(api.payload, search_isbn)
        b = Books.query.filter_by(isbn=api.payload['isbn']).first()
        if b is not None:
            return b, 200
        else:
            api.abort(404)


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