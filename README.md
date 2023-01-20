# Challange : Support Multiple Storage type to store data
## 1. Testing a Struct interface
Source code: `./stack/Stack.py`

Run client code: 

```
python stack/Stack.py
```

## 2. Data Store Library
### Install on local
1. Install dependencies

    ```
    pip install -r requirements.txt
    ```

2. Start service

    ```
    uvicorn service.main:app --host 0.0.0.0 --port 8000
    ```

3. Go to http://0.0.0.0:8000

### Run on docker
1. Build docker image

    ```
    docker build -t y42:latest .
    ```

2. Run container
    ```
    docker run --name y42Container -p 8000:80 -d y42:latest
    ```

3. Go to http://0.0.0.0:8000

### Notes
- Framework: FastAPI
- Implemented format: json
- Implemented storage: local storage
- Mocked format: xml
- Mocked storage: S3

I used strategy design pattern to manage data-formats(json,xml, etc.) and data-storages(localStorage, S3, etc.)

The main entity of this task is the DataModel. Each DataModel has it's own format(DataFormat abstract class) and destination(Storage abstract class).

- DataModel:

- DataFormat:

- Storage:

### Generate test coverage report

```
pytest --cov=../ --cov=stack --cov=DataStorage --cov-report=html tests
```
