from fastapi import APIRouter
from config import settings
from app.models import *
import json

router = APIRouter()

@router.post(
    "/w3c/vc-validator/1.1", 
    tags=["Modules"], 
    summary="VCDM 1.1 test-suite (Positive testing from the vc-test-suite)"
)
async def vc_validator_v1(test_suite_input: VCTestSuiteV1Input):
    vc_input = vars(test_suite_input)["vc_input"]
    # vc_input = json.dumps(vc_input)
    supported_features = vars(test_suite_input)["supported_features"]
    all_features = ["basic", "schema", "refresh", "evidence", "status", "tou", "ldp", "jwt", "zkp"]
    unsupported_features = [feature for feature in all_features if feature not in supported_features]
    # module_w3c.run_vc_validator(verifiable_credential=vc_input, sections_not_suppored=unsupported_features)
    return False