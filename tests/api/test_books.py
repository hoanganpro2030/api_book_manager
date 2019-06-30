import json

def test_get_all(client):
    response = client.get('/api/Books/')
    assert response.status_code == 200


def test_by_id(client):
    response = client.get('/api/Books/3')
    assert response.status_code == 200
    response = client.get('/api/Books/4')
    assert response.status_code == 404
    response = client.delete('/api/Books/3')
    assert response.status_code == 204
    response = client.delete('/api/Books/3')
    assert response.status_code == 404
    response = client.get('/api/Books/search/list/')
    assert response.status_code == 404

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'title': "sach 1",
        "isbn": "978-604-1-00000-2",
        "views": 5,
        "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
        "votes": 42,
        "downloads": 0,
        "status": True,
        "created": "Sat, 29 Jun 2019 13:15:35 -0000",
        "year": 2015,
        "author_id": 1,
        "id": 1
    }
    response = client.put('/api/Books/2', data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json['id'] == 2
    assert response.json['isbn'] == '978-604-1-00000-2'


# def test_post_books(client):
#     data = {
#         'last_name': "hoang thuong",
#         "first_name": "dang",
#         "phone": "0369327564",
#         "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
#         "id": 42,
#         "email": "hoangthuong@gmail.com",
#         "status": "true",
#         "created": "Sat, 29 Jun 2019 13:15:35 -0000",
#         "address": "Nha Trang"
#     }
#     response = client.post('/api/Authors/', data=json.dumps(data))
#     assert response.status_code == 201


def test_post_authors(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'title': "sach 1",
        "isbn": "978-604-1-00000-2",
        "views": 5,
        "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
        "votes": 42,
        "downloads": 0,
        "status": True,
        "created": "Sat, 29 Jun 2019 13:15:35 -0000",
        "year": 2015,
        "author_id": 1,
        "id": 1
    }
    response = client.post('/api/Books/', data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json['isbn'] == "978-604-1-00000-2"

    data = {
        'title': "sach 2",
        "isbn": "978-604-1-00000-2",
        "views": 5,
        "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
        "votes": 42,
        "downloads": 0,
        "status": True,
        "created": "Sat, 29 Jun 2019 13:15:35 -0000",
        "year": 2015,
        "author_id": 1,
        "id": 1
    }
    response = client.post('/api/Books/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json['message'] == "Invalid, ISBN already existed"

    data = {
        'title': "sach 3",
        "isbn": "978-604-3-00000-2",
        "year": 2015,
        "author_id": 1
    }
    response = client.post('/api/Books/', data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json['isbn'] == "978-604-3-00000-2"

    data = {
        "isbn": "978-604-4-00000-2",
        "year": 2015,
        "author_id": 1
    }
    response = client.post('/api/Books/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json['errors']['title'] == "'title' is a required property"

    data = {
        'title': "sach 5",
        "isbn": "978-604-5---000-2",
        "year": 2015,
        "author_id": 1,
    }
    response = client.post('/api/Books/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json['custom'] == "Validation of 'isbn' field failed"
    response = client.get('/api/Books/5')
    assert response.status_code == 200
    response = client.get('/api/Books/6')
    assert response.status_code == 404