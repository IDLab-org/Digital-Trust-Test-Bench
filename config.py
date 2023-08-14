from pydantic import BaseSettings
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Settings(BaseSettings):
    PROJECT_TITLE = "DTT API Service"
    PROJECT_VERSION = "v0"
    PROJECT_DESCRIPTION = """
    API service for the DDT platform
    """
    PROJECT_CONTACT = {
        "name": "IDLab",
        "url": "https://idlab.org",
    }
    PROJECT_LICENSE_INFO = {
        "name": "DTT-Service",
        "url": "https://github.com/IDLab-org/DTT-Service",
    }

    DEMO_USER = {
        "username": "demo.user",
        "password": "password123"
    }

settings = Settings()
