# DTT-Frontend

Front End app for the DTT Bench

## Running locally
Pre-requisites:
- python3.11
- python3.11-venv

### Set up a python 3.11 virtual environment & install dependencies
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

### To access reporting, you need to port-forward the allure service from your designated namespace
```
kubctl port-forward svc/allure 5050:5050
```

### To enable the session storage, you need to port-forward the redis service from the dtt-storage namespace
```
kubectl port-forward -n dtt-storage svc/redis 6379:6379
```

### Run the application
```python start.py```

- The application will be running at [http://localhost:5000](http://localhost:5000)
- Your allure private instance will be running at [http://localhost:5050](http://localhost:5050)

### DTT-DEV Internal Endpoints (VPN Connection required)
- DTT-Frontend: [http://dtt-dev.internal.idlab.org:5000](http://dtt-dev.internal.idlab.org:5000)
- DTT-Service: [http://dtt-dev.internal.idlab.org:8000](http://dtt-dev.internal.idlab.org:8000)

### DTT-Cloud Endpoints
- VC-API: [https://vc-api.dtt-cloud.idlab.app](https://vc-api.dtt-cloud.idlab.app)
- ACApy Agent Admin Interface: [https://agent-admin.dtt-cloud.idlab.app](https://agent-admin.dtt-cloud.idlab.app)

