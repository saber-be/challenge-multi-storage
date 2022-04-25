from typing import Dict, List, Optional, Union
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from enum import Enum
import DataStorage.DataStorage as DataStorage

description = """
## Data Store Library
A library that can be used to store and retrieve arbitrary data in multiple formats & destinations.
- **Swagger UI: [/docs](/docs)**
- **ReDoc UI: [/redoc](/redoc)**
"""

tags_metadata = [
    {
        "name": "DataStorage APIs",
    },
    {
        "name": "redirects",
    },
]

class SupportedFormats(str, Enum):
    json = "json"
    xml = "xml_mock"

class SupportedStorages(str, Enum):
    localStorage = "localStorage"
    S3= "S3_mock"


formats: Dict[str, DataStorage.DataFormat] = {
    "json": DataStorage.JsonDataFormat(),
    "xml_mock" : DataStorage.MockXMLDataFormat()
}

storages: Dict[str,DataStorage.Storage] = {
    "localStorage": DataStorage.LocalStorage(config={"path": "./DataStorage/"}),
    "S3_mock": DataStorage.MockStorage(config={"bucket": "y42", "accessKey": "accessKey", "secretKey": "secretKey", "path": "y42.s3.amazonaws.com/DataStorage/"})
}

app = FastAPI(title="Data Store Library",
              description=description,
              openapi_tags=tags_metadata)




@app.post("/query/{storage}/{format}/", response_model=List[dict], description="Run query on DataStorage", tags=["DataStorage APIs"])
async def query(query:dict,format:SupportedFormats = SupportedFormats.json,storage:SupportedStorages = SupportedStorages.localStorage,limit:Optional[int]=5,offset:Optional[int] = 0) -> List[dict]:
    model = DataStorage.DataModel()
    model.format = formats.get(format,formats.get("json"))
    data_storage = storages.get(storage,storages.get("localStorage"))
    model.storage = data_storage 
    
    return model.query(query,limit,offset)

@app.post("/insert/{storage}/{format}/", response_model=str, description="Insert record into DataStorage", tags=["DataStorage APIs"])
async def insert(record:dict,format:SupportedFormats = SupportedFormats.json,storage:SupportedStorages = SupportedStorages.localStorage) -> str:
    model = DataStorage.DataModel()
    model.format = formats.get(format,formats.get("json"))
    model.storage = storages.get(storage,storages.get("localStorage"))
    model.insert(record)
    return f"Record inserted into {model.storage.__class__.__name__}:{model.getPath()}"


@app.post("/batchInsert/{storage}/{format}/", response_model=str, description="Insert records into DataStorage", tags=["DataStorage APIs"])
async def batchInsert(records:List[dict],format:SupportedFormats = SupportedFormats.json,storage:SupportedStorages = SupportedStorages.localStorage) -> str:
    model = DataStorage.DataModel()
    model.format = formats.get(format,formats.get("json"))
    model.storage = storages.get(storage,storages.get("localStorage"))
    model.batchInsert(records)
    return f"Records inserted into {model.storage.__class__.__name__}:{model.getPath()}"

@app.delete("/delete/{storage}/{format}/", response_model=List[Dict[str, Union[str, int, float,bool]]], tags=["DataStorage APIs"])
def delete(storage: SupportedStorages, format: SupportedFormats, query: Dict[str, Union[str, int, float,bool]]):
    model = DataStorage.DataModel()
    model.storage = storages[storage]
    model.format = formats[format]
    model.delete(query)
    return model.data

@app.get("/", response_class=RedirectResponse, tags=["redirects"])
async def docs_redirect():
    return '/docs'
