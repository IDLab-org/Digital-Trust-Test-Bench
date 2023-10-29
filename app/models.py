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

class VCTestSuiteV1Input(BaseModel):
    vc_input: dict = Field(alias="input", example=vc_input) 
    supported_features: list = Field(example=["basic", "schema", "refresh", "evidence", "status", "tou", "ldp", "jwt", "zkp"])



class CreateWorkspaceInput(BaseModel):
    name: str = Field(example="my_workspace") 