from fastapi.testclient import TestClient
from DataStorage.main import app
import pytest
client = TestClient(app)

def test_query():

    query = {}
    response = client.post("/query/S3_mock/xml_mock/?limit=5&offset=0", json=query)
    correct_response = [
        {
            "id": 1,
            "name": "saber",
            "lname": "bej"
        },
        {
            "id": 2,
            "name": "john",
            "lname": "doe"
        }
    ]

    assert response.status_code == 200
    assert response.json() == correct_response

def test_query_limit():

    query = {}
    response = client.post("/query/S3_mock/xml_mock/?limit=1&offset=0", json=query)
    correct_response = [
        {
            "id": 1,
            "name": "saber",
            "lname": "bej"
        }
    ]

    assert response.status_code == 200
    assert response.json() == correct_response

def test_query_offset():

    query = {}
    response = client.post("/query/S3_mock/xml_mock/?limit=5&offset=1", json=query)
    correct_response = [
        {
            "id": 2,
            "name": "john",
            "lname": "doe"
        }
    ]

    assert response.status_code == 200
    assert response.json() == correct_response




def test_insert_into_mock_storage():
    data = {"name":"saber","lname":"bej","role":"developer"}
    
    response = client.post("/insert/S3_mock/xml_mock/", json=data)

    assert response.status_code == 200
    assert "Record inserted into MockStorage:y42.s3.amazonaws.com/DataStorage/data.xml" in response.text

def test_insert():
    #make storage empty
    client.delete("/delete/localStorage/json/", json={})

    #insert record into storage
    data = {"name":"saber","lname":"bej","role":"developer"}
    client.post("/insert/localStorage/json/", json=data)
    
    #check if record is in storage
    query_response = client.post("/query/localStorage/json/?limit=5&offset=0", json={})
    all_data_in_local_storage = query_response.json() 
    assert data in all_data_in_local_storage

def test_batchInsert():
    #make storage empty
    client.delete("/delete/localStorage/json/", json={})

    #insert record into storage
    data = [{"name":"saber","lname":"bej","role":"developer"},{"name":"john","lname":"doe","role":"developer"}]
    client.post("/batchInsert/localStorage/json/", json=data)
    
    #check if record is in storage
    query_response = client.post("/query/localStorage/json/?limit=5&offset=0", json={})
    all_data_in_local_storage = query_response.json() 
    for record in data:
        assert record in all_data_in_local_storage