from DataStorage.DataStorage import DataModel
from DataStorage.DataStorage import JsonDataFormat, MockXMLDataFormat, MockStorage, LocalStorage

def test_query():
    model = DataModel()
    model.format = MockXMLDataFormat()
    model.storage = MockStorage(config={"path": "./DataStorage/"})
    
    query = {}
    assert model.query(query) == [{"id":1,"name":"saber","lname":"bej"},{"id":2,"name":"john","lname":"doe"}]

    query = {"id":1}
    assert model.query(query) == [{"id":1,"name":"saber","lname":"bej"}]

def test_insert():
    model = DataModel()
    model.format = MockXMLDataFormat()
    model.storage = MockStorage(config={"path": "./DataStorage/"})
    
    data = {"id":3,"name":"saber","lname":"bej"}
    model.data = [{"id":1,"name":"saber","lname":"bej"},{"id":2,"name":"john","lname":"doe"}]
    assert data not in model._data 
    model.insert(data)
    assert data in model._data 

def test_delete():
    model = DataModel()
    model.format = MockXMLDataFormat()
    model.storage = MockStorage(config={"path": "./DataStorage/"})
    
    query = {"id":1}
    model.data = [{"id":1,"name":"saber","lname":"bej"},{"id":2,"name":"john","lname":"doe"}]
    assert {"id":1,"name":"saber","lname":"bej"} in model._data 
    model.delete(query)
    assert {"id":1,"name":"saber","lname":"bej"} not in model._data 


def test_batchInsert():
    model = DataModel()
    model.format = MockXMLDataFormat()
    model.storage = MockStorage(config={"path": "./DataStorage/"})
    
    data = [{"id":3,"name":"saber","lname":"bej"},{"id":4,"name":"john","lname":"doe"}]
    model.data = [{"id":1,"name":"saber","lname":"bej"},{"id":2,"name":"john","lname":"doe"}]
    for record in data:
        assert record not in model._data 
    model.batchInsert(data)
    for record in data:
        assert record in model._data

