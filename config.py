import os, redis, json
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    ENV = os.environ["ENV"]
    DEBUG = os.environ["DEBUG"]
    TESTING = os.environ["TESTING"]
    SECRET_KEY = os.environ["SECRET_KEY"]

    # Backend API
    DTT_SERVICE_URL = os.environ["DTT_SERVICE_URL"]

    # Flask-session with redis
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url(os.environ["REDIS_URL"])
    SESSION_COOKIE_NAME = "dtt-dev"

    # File upload security
    UPLOAD_EXTENSIONS = [".json", ".jsonld"]
    MAX_CONTENT_LENGTH = 1024 * 1024

    with open("app/static/data/pres_req/user.json", "r") as f:
        LOGIN_PRESENTATION_REQUEST = json.load(f)

    with open("app/static/data/cred_offer/user.json", "r") as f:
        ACCOUNT_CREDENTIAL_OFFER = json.load(f)

    # VC login issuer/verifier
    VC_API_ENDPOINT = os.environ["VC_API_ENDPOINT"]
    AGENT_ENDPOINT = os.environ["AGENT_ENDPOINT"]
    AGENT_ADMIN_ENDPOINT = os.environ["AGENT_ADMIN_ENDPOINT"]

    BACKCHANNEL_IMAGES = ["afj", "acapy", "afgo", "dotnet", "vcx", "findy"]
