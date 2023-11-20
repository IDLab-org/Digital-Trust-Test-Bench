from fastapi import APIRouter, Request
from app.models import *
from app.controllers import k8s
import hashlib, requests

router = APIRouter()


@router.get("/backchannels", tags=["AATH"], summary="List Backchannels")
async def list_backchannels():
    namespaces = k8s.list_namespaces()
    namespaces = [namespace for namespace in namespaces if "workspace" in  namespace]
    return namespaces


@router.post("/backchannels", tags=["AATH"], summary="Deploy Backchannel")
async def deploy_backchannel(backchannel_input: DeployBackchannelInput):
    workspace_id = vars(backchannel_input)["workspace_id"]
    framework = vars(backchannel_input)["framework"]
    backchannel_info = settings.AATH_BACKCHANNELS[framework]
    backchannel_info["label"] = vars(backchannel_input)["label"]
    backchannel_info["public_endpoint"] = f"aath-backchannel-{framework}-{workspace_id.split('-')[-1]}.dtt-dev.idlab.app"
    k8s.deploy_backchannel(
        workspace_id,
        backchannel_info,
        settings.AATH_LEDGER_URL,
        settings.AATH_TAILS_URL
        )
    return ""


@router.post("/test-harness", tags=["AATH"], summary="Run Test Harness")
async def run_test_harness(test_harness_input: RunTestHarnessInput):
    return ""