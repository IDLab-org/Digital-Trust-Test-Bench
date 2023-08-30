# DTT-Frontend

Front End app for the DTT Bench
Currently an empty implementation with only a few routes

### Running locally
A -setup a virtual environment (if not done already)
    (From the .../DTT-Frontend folder)
    $ python3 -m venv venv
    
B - Update dependencies:
    $ source venv/bin/activate  
    $ pip3 install -r requirements.txt

C - Setup environment:
    $ source venv/bin/activate  (if not already activated)
    $ export FLASK_APP=start

D - Create the .env file (if not already done)
    Use .env.example as a starting point,. copy into a file called .env
    Fill-up values and save
            # Environment / Development settings
            ENV=development
            DEBUG=true
            TESTING=true
            SECRET_KEY="ToBeModified"
            DTT_SERVICE_URL="http://localhost:8000"  # (Assumed to point to a local version of the DTT service - no trailing slash)

E - Run the app in debug mode:
    $ flask run --debug