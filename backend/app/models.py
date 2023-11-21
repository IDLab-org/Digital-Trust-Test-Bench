from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from config import settings
import json

# with open("app/data/vc.jsonld", "r") as f:
#     vc_input = json.loads(f.read())

vc_input = {
    "@context": [
      "https://www.w3.org/2018/credentials/v1",
      "https://www.w3.org/2018/credentials/examples/v1"
    ],
    "id": "http://example.edu/credentials/58473",
    "type": ["VerifiableCredential", "AlumniCredential"],
    "issuer": "https://example.edu/issuers/14",
    "issuanceDate": "2010-01-01T19:23:24Z",
    "credentialSubject": {
      "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
      "alumniOf": "Example University"
    },
    "proof": {
      "type": "RsaSignature2018"
    }
  }

class VCDataModelV1Input(BaseModel):
    workspace_id: str = ''
    verifiable_credential: dict = vc_input
    # supported_features: list = Field(example=["basic", "schema", "refresh", "evidence", "status", "tou", "ldp", "jwt", "zkp"])


class VCTestSuiteV1Input(BaseModel):
    workspace_id: str = ''
    endpoint: str = ""
    token: str = ""
    unsupported_features: list = ["basic", "schema", "refresh", "evidence", "status", "tou", "ldp", "jwt", "zkp"]

class VCPlaygroundTestSuite(BaseModel):
    workspace_id: str = ''
    issuer: dict = {
        "id": "MATTR",
        "label": "MATTR",
        "endpoint": "https://platform.interop.mattrlabs.io/vc-http-api/v1/credentials",
    }
    verifier: dict = {
        "id": "MATTR",
        "label": "MATTR",
        "endpoint": "https://platform.interop.mattrlabs.io/vc-http-api/v1/credentials/verify",
    }


class CreateWorkspaceInput(BaseModel):
    workspace_label: str = Field(example="demo.user@idlab.org") 
    workspace_type: str = Field(example="private") 


class DeployBackchannelInput(BaseModel):
    workspace_id: str = Field(example="workspace-private-64220bf6a52c71843475d6dee399cb9a")
    framework: str = Field(example="vcx")
    label: str = Field(example="Reference VCX Backchannel")


class RunTestHarnessInput(BaseModel):
    tags: list = Field(example=["@issue-credential"])
    agents: list = Field(example=[])