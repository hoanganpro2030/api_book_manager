# coding=utf-8
import logging

import pytest

from base_task.admin.models import Authors, Books
__author__ = 'Kien'
_logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def app(request):
    from base_task import app
    from base_task.models import db
    print("Start app and init db.......")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12111998@localhost:3306/test'

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    # test db initializations go below here
    db.create_all()
    author = Authors(first_name='first_name',
                     last_name='last_name',
                     email='email@gmal.com',
                     phone='1234567890',
                     address='address')
    author1 = Authors(first_name='first_name',
                     last_name='last_name',
                     email='email1@gmal.com',
                     phone='12345678901',
                     address='address')
    author2 = Authors(first_name='first_name',
                     last_name='last_name',
                     email='email2@gmal.com',
                     phone='12345678902',
                     address='address')

    db.session.add(author)
    db.session.add(author1)
    db.session.add(author2)
    db.session.commit()

    book0 = Books(title='first_name',
                    isbn='978-604-0-00000-2',
                    year=2017,
                    author_id=1)
    book1 = Books(title='first_name1',
                    isbn='978-604-0-00200-2',
                    year=2017,
                    author_id=1)
    book2 = Books(title='first_name2',
                    isbn='978-604-0-00100-2',
                    year=2017,
                    author_id=1)
    db.session.add(book0)
    db.session.add(book1)
    db.session.add(book2)
    db.session.commit()

    def teardown():
        print("Tear down db")
        db.session.remove()
        db.drop_all()
        ctx.pop()

    yield app

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def client(app):
    return app.test_client()
