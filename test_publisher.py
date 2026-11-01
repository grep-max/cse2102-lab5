import pytest

import publisher


@pytest.fixture
def client():
  # Reset the publisher's in-memory state before every test
  publisher.subscribers.clear()
  publisher.subject = ""
  publisher.app.config['TESTING'] = True
  with publisher.app.test_client() as client:
    yield client


def addSubscriber(client, name, URI):
  return client.post('/add-subscriber', json={'name': name, 'URI': URI})


def test_home(client):
  response = client.get('/')
  assert response.status_code == 200
  assert b"Hello from Flask!" in response.data


def test_add_subscriber(client):
  response = addSubscriber(client, 'Grace', 'http://grace.example.com')
  assert response.status_code == 201
  assert publisher.subscribers == {'Grace': 'http://grace.example.com'}


def test_add_subscriber_overwrites_existing_name(client):
  addSubscriber(client, 'Grace', 'http://old.example.com')
  addSubscriber(client, 'Grace', 'http://new.example.com')
  assert publisher.subscribers == {'Grace': 'http://new.example.com'}


def test_add_subscriber_missing_fields(client):
  assert client.post('/add-subscriber', json={'name': 'Grace'}).status_code == 400
  assert client.post('/add-subscriber', json={'URI': 'http://x.com'}).status_code == 400
  assert client.post('/add-subscriber', data='not json').status_code == 400
  assert publisher.subscribers == {}


def test_list_subscribers(client):
  addSubscriber(client, 'Grace', 'http://grace.example.com')
  addSubscriber(client, 'Ada', 'http://ada.example.com')
  addSubscriber(client, 'Alan', 'http://example.com')
  response = client.get('/list-subscribers')
  assert response.status_code == 200
  assert response.get_json() == {'subscribers': {
    'Grace': 'http://grace.example.com',
    'Ada': 'http://ada.example.com',
    'Alan': 'http://example.com',
  }}


def test_list_subscribers_empty(client):
  response = client.get('/list-subscribers')
  assert response.status_code == 200
  assert response.get_json() == {'subscribers': {}}


def test_delete_subscriber(client):
  addSubscriber(client, 'Grace', 'http://grace.example.com')
  addSubscriber(client, 'Ada', 'http://ada.example.com')
  response = client.delete('/delete-subscriber', json={'name': 'Grace'})
  assert response.status_code == 200
  assert publisher.subscribers == {'Ada': 'http://ada.example.com'}


def test_delete_unknown_subscriber(client):
  addSubscriber(client, 'Ada', 'http://ada.example.com')
  response = client.delete('/delete-subscriber', json={'name': 'Bob'})
  assert response.status_code == 404
  assert publisher.subscribers == {'Ada': 'http://ada.example.com'}


def test_delete_subscriber_missing_name(client):
  response = client.delete('/delete-subscriber', json={})
  assert response.status_code == 400


def test_update_and_notify(client, capsys):
  addSubscriber(client, 'Grace', 'http://grace.example.com')
  addSubscriber(client, 'Ada', 'http://ada.example.com')
  response = client.post('/update-and-notify', json={'subject-update': 'buy IBM'})
  assert response.status_code == 200
  assert response.get_json()['notified'] == ['Grace', 'Ada']
  assert publisher.subject == 'buy IBM'
  assert client.get('/subject').get_json() == {'subject': 'buy IBM'}

  output = capsys.readouterr().out
  assert "Notifying Grace at http://grace.example.com of the new subject: buy IBM" in output
  assert "Notifying Ada at http://ada.example.com of the new subject: buy IBM" in output


def test_deleted_subscriber_is_not_notified(client, capsys):
  addSubscriber(client, 'Grace', 'http://grace.example.com')
  addSubscriber(client, 'Ada', 'http://ada.example.com')
  client.delete('/delete-subscriber', json={'name': 'Grace'})
  response = client.post('/update-and-notify', json={'subject-update': 'sell IBM'})
  assert response.get_json()['notified'] == ['Ada']
  assert "Notifying Grace" not in capsys.readouterr().out


def test_update_and_notify_missing_subject(client):
  response = client.post('/update-and-notify', json={})
  assert response.status_code == 400
  assert publisher.subject == ""
