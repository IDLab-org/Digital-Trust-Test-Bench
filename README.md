# DTT-Service

API backend for the DTT Bench

Currently an empty implementation with only 1 route: 
- /login   - Fake login, added to establish and test a basic interaction between the Front End app and this service

## Running locally
Pre-requisites:
- python3.11
- python3.11-venv

### Setting up a virtual environment & install dependencies
```
python3.11 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```

### Run the application
```uvicorn main:app --reload --host 0.0.0.0```

- The application will be running at [http://localhost:8000](http://localhost:8000)
- Openapi doc availiable at [http://localhost:8000/docs](http://localhost:8000/docs)

### DTT-DEV Internal Endpoints
- DTT-Frontend: [http://dtt-dev.internal.idlab.org:5000](http://dtt-dev.internal.idlab.org:5000)
- DTT-Service: [http://dtt-dev.internal.idlab.org:8000](http://dtt-dev.internal.idlab.org:8000)