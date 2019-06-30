from base_task.admin.models import Authors
import json

def test_get_all(client):
    response = client.get('/api/Authors/')
    assert response.status_code == 200


def test_by_id(client):
    response = client.get('/api/Authors/3')
    assert response.status_code == 200
    response = client.get('/api/Authors/4')
    assert response.status_code == 404
    response = client.delete('/api/Authors/3')
    assert response.status_code == 204
    response = client.delete('/api/Authors/3')
    assert response.status_code == 404

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'last_name': "hoang thuong",
        "first_name": "dang",
        "phone": "0369327564",
        "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
        "id": 42,
        "email": "hoangthuong@gmail.com",
        "status": True,
        "created": "Sat, 29 Jun 2019 13:15:35 -0000",
        "address": "Nha Trang"
    }
    response = client.put('/api/Authors/2', data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json['id'] == 2
    assert response.json['phone'] == '0369327564'

def test_post_authors(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'last_name': "hoang thuong",
        "first_name": "dang",
        "phone": "0369327564",
        "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
        "id": 42,
        "email": "hoangthuong@gmail.com",
        "status": True,
        "created": "Sat, 29 Jun 2019 13:15:35 -0000",
        "address": "Nha Trang"
    }
    response = client.post('/api/Authors/', data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json['email'] == "hoangthuong@gmail.com"

    data = {
        'last_name': "hoang thuong 1",
        "first_name": "dang 1",
        "phone": "0369327564",
        "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
        "id": 42,
        "email": "hoangthuong1@gmail.com",
        "status": True,
        "created": "Sat, 29 Jun 2019 13:15:35 -0000",
        "address": "Nha Trang"
    }
    response = client.post('/api/Authors/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json['message'] == "Phone have already existed"

    data = {
        'last_name': "hoang thuong 1",
        "first_name": "dang 1",
        "phone": "0369327567",
        "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
        "id": 42,
        "email": "hoangthuong@gmail.com",
        "status": True,
        "created": "Sat, 29 Jun 2019 13:15:35 -0000",
        "address": "Nha Trang"
    }
    response = client.post('/api/Authors/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json['message'] == "Email have already existed"

    data = {
        'last_name': "hoang thuong 2",
        "phone": "0369327560",
        "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
        "id": 42,
        "email": "hoangthuong2@gmail.com",
        "status": True,
        "created": "Sat, 29 Jun 2019 13:15:35 -0000",
        "address": "Nha Trang"
    }
    response = client.post('/api/Authors/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json['message'] == "Input payload validation failed"

    data = {
        'last_name': "hoang thuong 3",
        "phone": "0369327563",
        "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
        "id": 42,
        "email": "hoangthuong3gmail.com",
        "status": True,
        "created": "Sat, 29 Jun 2019 13:15:35 -0000",
        "address": "Nha Trang"
    }
    response = client.post('/api/Authors/', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json['message'] == "Input payload validation failed"
    response = client.get('/api/Authors/4')
    assert response.status_code == 200
    response = client.get('/api/Authors/5')
    assert response.status_code == 404




