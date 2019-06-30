

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


# def test_post_books(client):
#     response = client.post('/api/Authors/', data={"last_name": "hoang thuong",
#                                                     "first_name": "dang",
#                                                     "phone": "0369327564",
#                                                     "updated": "Sat, 29 Jun 2019 13:15:35 -0000",
#                                                     "id": 42,
#                                                     "email": "hoangthuong@gmail.com",
#                                                     "status": "true",
#                                                     "created": "Sat, 29 Jun 2019 13:15:35 -0000",
#                                                     "address": "Nha Trang"})
#     assert response.status_code == 201
