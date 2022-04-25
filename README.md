# Y42 Coding Challenge
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
### Generate test coverage report

```
pytest --cov=../ --cov=stack --cov=DataStorage --cov-report=html tests
```