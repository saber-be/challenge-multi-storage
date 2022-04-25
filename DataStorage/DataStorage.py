from __future__ import annotations
from abc import ABC, abstractmethod
from distutils import extension
from typing import List
import json
import threading
import time
from multiprocessing import Lock
from xml.etree.ElementTree import Element as XMLElement

class DataFormat(ABC):
    extension:str

    @staticmethod
    @abstractmethod
    def FromBytes(data:bytes) -> List[dict]:
        ...

    @staticmethod
    @abstractmethod
    def ToBytes(data:List[dict]) -> bytes:
        ...

class JsonDataFormat(DataFormat):
    extension:str = "json"
    @staticmethod
    def FromBytes(data:bytes) -> List[dict]:
        if (len(data)) == 0:
            return []
        return json.loads(data.decode("utf-8"))

    @staticmethod
    def ToBytes(data:List[dict]) -> bytes:
        return json.dumps(data).encode("utf-8")

class MockXMLDataFormat(DataFormat):
    extension:str = "xml"
    @staticmethod
    def FromBytes(data:bytes) -> List[dict]:
        return [{"id":1,"name":"saber","lname":"bej"},{"id":2,"name":"john","lname":"doe"}]

    @staticmethod
    def ToBytes(data:List[dict]) -> bytes:
        return """<?xml version="1.0" encoding="UTF-8" ?>
        <root>
            <row>
                <id>1</id>
                <name>saber</name>
                <lname>bej</lname>
            </row>
            <row>
                <id>2</id>
                <name>john</name>
                <lname>doe</lname>
            </row>
        </root>
        """.replace("        <","<").encode("utf-8")

class Storage(ABC):
    _config:dict
    def threadsafe(func):
        """decorator making sure that the decorated function is thread safe"""
        lock = Lock()
        def new(*args,**kwargs):
            print(lock.__dict__)
            lock.acquire()
            print("lock aquired")
            try:
                r = func(*args, **kwargs)   
                # time.sleep(5)
            except Exception as e:
                raise e
            finally:
                lock.release()
            return r
        return new

    @property
    def config(self) -> dict:
        return self._config
    
    @config.setter
    def config(self, config:dict) -> None:
        self._config = config
        
    @threadsafe
    def read(self, path:str) -> bytes:
        ...

    @threadsafe
    def write(self, data:bytes, path:str) -> None:
        ...

class LocalStorage(Storage):
    
    def __init__(self, config:dict):
        self.config = config

    
    @Storage.threadsafe
    def read(self,path:str) -> bytes:
        """
        Try to read the file. If the file does not exist, return an empty byte array.
        """
        
        try: 
            with open(path, "rb") as f:
                return f.read()
        except FileNotFoundError as e:
            print(str(e))
            return b""

    @Storage.threadsafe
    def write(self, data:bytes,path:str) -> None:
        with open(path, "wb") as f:
            f.write(data)

class MockStorage(Storage):
    def __init__(self, config:dict):
        self.config = config

    @Storage.threadsafe
    def read(self,path:str) -> bytes:
        print("Reading from mock storage")
        return b''

    @Storage.threadsafe
    def write(self, data:bytes,path:str) -> None:
        print("Data has been written to the mock storage")



class DataModel():

    _format : DataFormat
    _storage : Storage
    _data : List[dict]
    
    @property
    def data(self) -> DataFormat:
        return self.format.FromBytes(self.storage.read(path = self.getPath()))

    @data.setter
    def data(self, data:List[dict]) -> None:
        if data is None:
            raise Exception("Data cannot be None")
        self._data = data
        self.storage.write(data = self.format.ToBytes(self._data), path = self.getPath())

    @property
    def format(self) -> DataFormat:
        return self._format

    @format.setter
    def format(self, format:DataFormat) -> None:
        self._format = format

    def getPath(self) -> str:
        return self.storage.config["path"] + "data." + self.format.extension

    @property
    def storage(self) -> Storage:
        return self._storage

    @storage.setter
    def storage(self, storage:Storage) -> None:
        self._storage = storage

    def query(self, query:dict,limit:int=5,offset:int=0) -> List[dict]:
        return [d for d in self.data if all(d.get(k) == v for k, v in query.items())][offset:offset+limit]
    
    def delete(self, query:dict) -> List[dict]:
        self.data = [d for d in self.data if not all(d.get(k) == v for k, v in query.items())]

    def insert(self, data:dict) -> None:
        self.data += [data]
        
    def batchInsert(self, data:List[dict]) -> None:
        self.data += data
        
    def __repr__(self) -> str:
        return str(self.data)


if __name__ == "__main__": # pragma: no cover

    model = DataModel()
    model.format = JsonDataFormat()
    model.storage = LocalStorage({"file": "./data3.json"})
    
    # data = model.data
    print(model)
    data = []
    data.append({"value": 0, "currency": "USD"})
    data.append({"value": 11, "currency": "USD"})
    model.insert(data[0])
    print(model)
    # model.write(data)
    # t1 = threading.Thread(target=model.data, args=(data,))

    filtered = model.query({"value": 11})
    print(filtered)
    model.delete({"value": 1})
    # t1.start()
    print(model)
    # print(model.delete({"value": 11, "currency": "USD"}))
    # t2 = threading.Thread(target=model.data, args=(data,))
    # t2.start()
    # t1.join()
    # t2.join()
    # print(filtered)
    

    # Storage.insert({'name': 'John', 'age': '22'})
    # Storage.batchInsert([{'name': 'John', 'age': '22'}, {'name': 'John', 'age': '22'}])
