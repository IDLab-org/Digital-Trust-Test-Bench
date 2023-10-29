from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from config import settings
import json

with open("data/vc.jsonld", "r") as f:
    vc_input = json.loads(f.read())



class VCTestSuiteV1Input(BaseModel):
    vc_input: dict = Field(alias="input", example=vc_input) 
    supported_features: list = Field(example=["basic", "schema", "refresh", "evidence", "status", "tou", "ldp", "jwt", "zkp"])



class CreateWorkspaceInput(BaseModel):
    name: str = Field(example="my_workspace") 