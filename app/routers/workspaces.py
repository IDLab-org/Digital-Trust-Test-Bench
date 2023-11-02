from fastapi import APIRouter, Request
from app.models import *
from app.controllers import k8s
import hashlib, requests

router = APIRouter()


@router.get("", tags=["Workspaces"], summary="List Workspaces")
async def list_workspaces():
    namespaces = k8s.list_namespaces()
    namespaces = [namespace for namespace in namespaces if "workspace" in  namespace]
    return namespaces

@router.post(
    "", 
    tags=["Workspaces"], 
    summary="Create workspace"
)
async def create_workspace(create_workspace_input: CreateWorkspaceInput, request: Request, workspace_type: str = None):
    workspace_label = vars(create_workspace_input)["workspace_label"]
    workspace_type = vars(create_workspace_input)["workspace_type"]
    workspace_id = hashlib.md5(workspace_label.encode('utf-8')).hexdigest()
    namespace = f"workspace-{workspace_type}-{workspace_id}"
    # status = requests.post(f"https:///workspaces?type={workspace_type}&id={workspace_id}")

    # Create namespace
    k8s.create_namespace(namespace)

    # Create allure server
    k8s.deploy_allure_server(namespace)

    # # Create reference backchannels
    # k8s.deploy_backchannel(namespace, "acapy")
    # k8s.deploy_backchannel(namespace, "afj")

    return {"workspace_id": namespace}

# @router.delete(
#     "", 
#     tags=["Workspaces"], 
#     summary="Delete workspace"
# )
# async def delete_workspace(create_workspace_input: CreateWorkspaceInput):
#     workspace = vars(create_workspace_input)
#     if workspace['scope'] not in ['private', 'organization']:
#         return "Invalid workspace scope"
#     namespace_id = hashlib.md5(workspace["name"].encode('utf-8')).hexdigest()
#     namespace = f"workspace-{workspace['scope']}-{namespace_id}"
#     status = k8s.delete_namespace(namespace)
#     return status