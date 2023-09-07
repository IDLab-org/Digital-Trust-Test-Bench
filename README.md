# DTT-Frontend

Front End app for the DTT Bench

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

### Create local .env file and fill in values
```cp .env.example .env```

Example values:
```
ENV=development
DEBUG=true
TESTING=true
SECRET_KEY=my_s3cret_key
DTT_SERVICE_URL=http://localhost:8000 # Use a running DTT-Service instance
```

### Run the application
```python start.py```

- The application will be running at [http://localhost:5000](http://localhost:5000)

### DTT-DEV Internal Endpoints
- DTT-Frontend: [http://dtt-dev.internal.idlab.org:5000](http://dtt-dev.internal.idlab.org:5000)
- DTT-Service: [http://dtt-dev.internal.idlab.org:8000](http://dtt-dev.internal.idlab.org:8000)
