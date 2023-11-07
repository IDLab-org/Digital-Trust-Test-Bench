from fastapi import APIRouter
from config import settings
from jinja2 import Environment, PackageLoader
from app.models import *
from app import utilities
from app.controllers import k8s
import yaml, json, requests

router = APIRouter()

@router.get(
    "/status", 
    tags=["Test-Suites"], 
    summary=""
)
async def test_suite_status(workspace_id: str, project_id: str):
    status = k8s.check_job_status(workspace_id, project_id)
    return status

@router.post(
    "/data-model", 
    tags=["Test-Suites"], 
    summary="VCDM 1.1 test-suite (Positive testing from the vc-test-suite)"
)
async def data_model(data_model_input: VCDataModelV1Input):
    workspace_id = vars(data_model_input)["workspace_id"]
    vc = vars(data_model_input)["verifiable_credential"]
    vc_profile, unsupported_features = utilities.vc_profiler(vc)
    k8s.launch_data_model_test_suite(
        namespace=workspace_id, 
        verifiable_credential=json.dumps(vc), 
        unsupported_features=json.dumps(unsupported_features)
        )
    return vc_profile

@router.post(
    "/vc-test-suite", 
    tags=["Test-Suites"], 
    summary="W3C vc-test-suite"
)
async def vc_test_suite(test_suite_input: VCTestSuiteV1Input):
    workspace_id = vars(test_suite_input)["workspace_id"]
    unsupported_features = vars(test_suite_input)["unsupported_features"]
    endpoint = vars(test_suite_input)["endpoint"]
    token = vars(test_suite_input)["token"]
    k8s.launch_vc_test_suite(
        namespace=workspace_id, 
        endpoint=endpoint, 
        token=token,
        unsupported_features=json.dumps(unsupported_features)
        )
    return ""

@router.post(
    "/vc-playground-test-suite", 
    tags=["Test-Suites"], 
    summary=""
)
async def vc_playground_test_suite(test_suite_input: VCPlaygroundTestSuite):
    workspace_id = vars(test_suite_input)["workspace_id"]
    issuer = vars(test_suite_input)["issuer"]
    verifier = vars(test_suite_input)["verifier"]
    k8s.launch_vc_playground_test_suite(
        namespace=workspace_id, 
        issuer=issuer, 
        verifier=verifier
        )
    return ""