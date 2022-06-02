from http import client
import pytest
from jose import jwt
from ..main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root(client):

     res = client.get("/")
     print(res.json().get('message'))
     assert res.json().get('message') == 'Hello World'
     assert res.status_code == 200