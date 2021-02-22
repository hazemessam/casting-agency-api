# Third party imports
import pytest

# Application imports
from app import app
from models import db, insert_dummy_data
from config import tokens


# Auth0 JWT tokens
casting_assistant_token = tokens.get('casting_assistant')
casting_director_token = tokens.get('casting_director')
executive_producer_token = tokens.get('executive_producer')


@pytest.fixture
def client():
    db.drop_all()
    db.create_all()
    insert_dummy_data()
    app.config['TESTING'] = True
    client = app.test_client()
    
    yield client


#---------------------------------
# Actor test cases
#---------------------------------

def test_get_all_actors(client):
    headers = {'Authorization': casting_assistant_token}
    res = client.get('/actors', headers=headers)
    assert res.status_code == 200
    assert res.json.get('actors') != None


def test_get_all_actors_without_token(client):
    res = client.get('/actors')
    assert res.status_code == 401


def test_create_actor(client):
    headers = {'Authorization': casting_director_token}
    body = {'name': 'Hazem', 'age':25, 'gender': 'male'}
    res = client.post('/actors', json=body, headers=headers)
    assert res.status_code == 201
    assert res.json.get('name') == 'Hazem'
    assert res.json.get('id') != None


def test_create_actor_without_permission(client):
    headers = {'Authorization': casting_assistant_token}
    body = {'name': 'Hazem', 'age':25, 'gender': 'male'}
    res = client.post('/actors', json=body, headers=headers)
    assert res.status_code == 401


def test_get_actor_by_id(client):
    headers = {'Authorization': casting_director_token}
    res = client.get('/actors/1', headers=headers)
    assert res.status_code == 200
    assert res.json.get('id') == 1


def test_get_unexisting_actor(client):
    headers = {'Authorization': casting_director_token}
    res = client.get('/actors/1000', headers=headers)
    assert res.status_code == 404


def test_update_actor(client):
    headers = {'Authorization': executive_producer_token}
    body = {'age': '25'}
    res = client.patch('/actors/1', json=body, headers=headers)
    assert res.status_code == 200
    assert res.json.get('age') == 25


def test_update_unexisting_actor(client):
    headers = {'Authorization': executive_producer_token}
    body = {'age': '25'}
    res = client.patch('/actors/1000', json=body, headers=headers)
    assert res.status_code == 404


def test_delete_actor(client):
    headers = {'Authorization': casting_director_token}
    res = client.delete('/actors/2', headers=headers)
    assert res.status_code == 200
    assert res.json.get('deleted') == 2


def test_delete_actor_without_permission(client):
    headers = {'Authorization': casting_assistant_token}
    res = client.delete('/actors/2')
    assert res.status_code == 401


def test_delete_unexisting_actor(client):
    headers = {'Authorization': casting_director_token}
    res = client.delete('/actors/1000', headers=headers)
    assert res.status_code == 404


# #---------------------------------
# # Movie test cases
# #---------------------------------

def test_get_all_movies(client):
    headers = {'Authorization': casting_assistant_token}
    res = client.get('/movies', headers=headers)
    assert res.status_code == 200
    assert res.json.get('movies') != None


def test_create_movie(client):
    headers = {'Authorization': executive_producer_token}
    body = {'title': 'Sherlock'}
    res = client.post('/movies', json=body, headers=headers)
    assert res.status_code == 201
    assert res.json.get('title') == 'Sherlock'
    assert res.json.get('id') != None


def test_create_movie_without_permission(client):
    headers = {'Authorization': casting_director_token}
    body = {'title': 'Sherlock'}
    res = client.post('/movies', json=body, headers=headers)
    assert res.status_code == 401
    

def test_create_existing_movie(client):
    headers = {'Authorization': executive_producer_token}
    body = {'title': 'Inside Out'}
    res = client.post('/movies', json=body, headers=headers)
    assert res.status_code == 422


def test_get_movie_by_id(client):
    headers = {'Authorization': casting_assistant_token}
    res = client.get('/movies/1', headers=headers)
    assert res.status_code == 200
    assert res.json.get('id') == 1


def test_get_unexisting_movie(client):
    headers = {'Authorization': executive_producer_token}
    res = client.get('/movies/1000', headers=headers)
    assert res.status_code == 404


def test_update_movie(client):
    headers = {'Authorization': casting_director_token}
    body = {'title': 'lions'}
    res = client.patch('/movies/1', json=body, headers=headers)
    assert res.status_code == 200
    assert res.json.get('id') == 1
    assert res.json.get('title') == 'Lions'


def test_update_unexisting_movie(client):
    headers = {'Authorization': executive_producer_token}
    body = {'title': 'Batman'}
    res = client.patch('/movies/1000',json=body, headers=headers)
    assert res.status_code == 404


def test_delete_movie(client):
    headers = {'Authorization': executive_producer_token}
    res = client.delete('/movies/2', headers=headers)
    assert res.status_code == 200
    assert res.json.get('deleted') == 2


def test_delete_unexisting_movie(client):
    headers = {'Authorization': executive_producer_token}
    res = client.delete('/movies/1000', headers=headers)
    assert res.status_code == 404
