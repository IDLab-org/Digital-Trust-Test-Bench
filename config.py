from pydantic import BaseSettings
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Settings(BaseSettings):
    PROJECT_TITLE = "DTT API Service"
    PROJECT_VERSION = "v0"
    PROJECT_DESCRIPTION = """
    API service for the DTT platform
    """
    PROJECT_CONTACT = {
        "name": "IDLab",
        "url": "https://idlab.org",
    }
    # PROJECT_LICENSE_INFO = {
    #     "name": "",
    #     "url": ""
    # }

    LOCAL:bool=os.environ["LOCAL"]
    VERSION=os.environ["VERSION"]
    SECRET_KEY=os.environ["SECRET_KEY"]
    DTT_FRONTEND_URL=os.environ["DTT_FRONTEND_URL"]
    OAUTH_GITHUB_CLIENT_ID=os.environ["OAUTH_GITHUB_CLIENT_ID"]
    OAUTH_GITHUB_CLIENT_SECRET=os.environ["OAUTH_GITHUB_CLIENT_SECRET"]

settings = Settings()
