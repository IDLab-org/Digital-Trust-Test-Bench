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

    VERSION=os.environ["VERSION"]
    SECRET_KEY=os.environ["SECRET_KEY"]
    DTT_FRONTEND_URL=os.environ["DTT_FRONTEND_URL"]
    OAUTH_GITHUB_CLIENT_ID=os.environ["OAUTH_GITHUB_CLIENT_ID"]
    OAUTH_GITHUB_CLIENT_SECRET=os.environ["OAUTH_GITHUB_CLIENT_SECRET"]

    AATH_LEDGER_URL = "http://test.bcovrin.vonx.io"
    AATH_TAILS_URL = "http://tails.bcovrin.vonx.io"
    AATH_BACKCHANNELS_BASE_ENDPOINT = "dtt-dev.idlab.app"
    AATH_BACKCHANNELS = {
        "vcx": {
            "framework": "vcx",
            "image": "idlaborg/aath-backchannel-vcx",
            "ports": [{
                "label": "backchannel",
                "port": "9020",
                "ingress": True
            }],
            "entrypoint": ["./aries-vcx-backchannel"],
            "endpoint": "http://aath-backchannel-vcx:9020"
            },
        "afj": {
            "framework": "afj",
            "image": "idlaborg/aath-backchannel-afj",
            "ports": [
                {
                    "label": "websocket",
                    "port": "9020",
                    "ingress": False
                },
                {
                    "label": "http",
                    "port": "9021",
                    "ingress": True
                },
                {
                    "label": "ws",
                    "port": "9022",
                    "ingress": False
                },
            ],
            "entrypoint": ["yarn", "ts-node", "src/index.ts"],
            "endpoint": "http://aath-backchannel-afj:9020"
            },
        "acapy": {
            "framework": "acapy",
            "image": "idlaborg/aath-backchannel-acapy",
            "ports": [
                {
                    "label": "backchannel",
                    "port": "8020",
                    "ingress": False
                },
                {
                    "label": "http",
                    "port": "8021",
                    "ingress": True
                },
                {
                    "label": "admin",
                    "port": "8022",
                    "ingress": False
                },
                {
                    "label": "webhooks",
                    "port": "8023",
                    "ingress": False
                },
                {
                    "label": "ws",
                    "port": "8024",
                    "ingress": False
                },
            ],
            "entrypoint": ["python", "acapy/acapy_backchannel.py"],
            "endpoint": "http://aath-backchannel-acapy:8020"
            },
        "afgo": {
            "framework": "afgo",
            "image": "idlaborg/aath-backchannel-afgo",
            "ports": [
                {
                    "label": "none",
                    "port": "8020",
                    "ingress": False
                },
                {
                    "label": "http",
                    "port": "8021",
                    "ingress": True
                },
                {
                    "label": "api",
                    "port": "8022",
                    "ingress": False
                },
                {
                    "label": "webhooks",
                    "port": "8023",
                    "ingress": False
                },
            ],
            "entrypoint": ["python", "afgo/afgo_backchannel.py"],
            "endpoint": "http://aath-backchannel-afgo:8022"
            },
        "dotnet": {
            "framework": "dotnet",
            "image": "idlaborg/aath-backchannel-dotnet",
            "ports": [{
                "label": "backchannel",
                "port": "9020",
                "ingress": True
            }],
            "entrypoint": ["dotnet", "DotNet.Backchannel.Master.dll"],
            "endpoint": "http://aath-backchannel-dotnet:9020"
            },
        # "findy": {
        #     "framework": "findy",
        #     "image": "idlaborg/aath-backchannel-findy",
        #     "ports": [{
        #         "label": "backchannel",
        #         "port": "8888",
        #         "ingress": True
        #     }]
        #     },
        }

    TEST_SUITES = {
        "vc-test-suite": {
            "image": "idlaborg/vc-test-suite:credivera-0.0.1"
        },
        "vc-playground-test-suite": {
            "image": "idlaborg/vc-playground-test-suite"
        },
        "aries-test-harness": {
            "image": "idlaborg/aries-test-harness"
        },
    }

settings = Settings()
