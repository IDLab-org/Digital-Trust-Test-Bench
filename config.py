import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config(object):
    ENV = os.environ["ENV"]
    DEBUG = os.environ["DEBUG"]
    TESTING = os.environ["TESTING"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    DTT_SERVICE_URL = os.environ["DTT_SERVICE_URL"]
    UPLOAD_EXTENSIONS = ['.json', '.jsonld']
    MAX_CONTENT_LENGTH = 1024 * 1024
    VC_API_ENDPOINT = os.environ["VC_API_ENDPOINT"]
    AGENT_ENDPOINT = os.environ["AGENT_ENDPOINT"]
    AGENT_ADMIN_ENDPOINT = os.environ["AGENT_ADMIN_ENDPOINT"]

    LOGIN_PRESENTATION_REQUEST = {
        "restriction_id": "VA56jZQD1V8dvhzD6vBqP4:3:CL:103060:User Credential",
        "attributes": [
            "email"
            ],
        "predicates": []
    }
    ACCOUNT_CREDENTIAL_OFFER = { 
        "credential": {
            "credentialSchema": {
                "id": "VA56jZQD1V8dvhzD6vBqP4:2:PlatformUserCredential:1.0",
                "definition": "VA56jZQD1V8dvhzD6vBqP4:3:CL:103060:User Credential"
            }
        }
    }
