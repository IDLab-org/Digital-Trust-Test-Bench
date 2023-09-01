# DTT-Service
API backend for the DTT Bench

Currently an empty implementation with only 1 route: 
    /login   - Fake login, added to establish and test a basic interaction between the Front End app and this service

### Running locally
A -setup a virtual environment (if not done already):
    (From the .../DTT-Service folder)
    $ python3 -m venv venv

    Must use Python 3.10 or higher

B - Update dependencies:
    $ source venv/bin/activate  
    $ pip3 install -r requirements.txt

C - Start the service:
`uvicorn main:app --reload --host 0.0.0.0`

D - See API docs using swagger:  
<ServiceURL>/docs