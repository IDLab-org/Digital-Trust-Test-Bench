from fastapi import APIRouter
from config import settings
from jinja2 import Environment, PackageLoader
from app.models import *
from app import utilities
from app.controllers import k8s
import yaml, json, requests

router = APIRouter()

@router.post(
    "/vc-test-suite", 
    tags=["Test-Suites"], 
    summary="VCDM 1.1 test-suite (Positive testing from the vc-test-suite)"
)
async def vc_test_suite(test_suite_input: VCTestSuiteV1Input):
    workspace_id = vars(test_suite_input)["workspace_id"]
    vc = vars(test_suite_input)["verifiable_credential"]
    vc_profile, unsupported_features = utilities.vc_profiler(vc)
    k8s.launch_vc_test_suite(
        namespace=workspace_id, 
        verifiable_credential=json.dumps(vc), 
        unsupported_features=json.dumps(unsupported_features)
        )
    return vc_profile

@router.get(
    "/vc-test-suite/status", 
    tags=["Test-Suites"], 
    summary="VCDM 1.1 test-suite (Positive testing from the vc-test-suite)"
)
async def vc_test_suite_status(workspace_id: str):
    status = k8s.check_vc_test_suite(workspace_id)
    return status

@router.post(
    "/vc-test-suite/report", 
    tags=["Test-Suites"], 
    summary="VCDM 1.1 test-suite (Positive testing from the vc-test-suite)"
)
async def vc_test_suite_status(workspace_id):
    r = requests.get(f"http://allure.{workspace_id}:5050/allure-docker-service/emailable-report/render?project_id=vc-test-suite")
    r = r.text
    r = r.replace("\n", "")
    r = r.replace("\\", "")
    return r