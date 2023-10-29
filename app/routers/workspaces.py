from fastapi import APIRouter, Request
from app.models import *
from app.k8s_controller import k8s
import hashlib, requests

router = APIRouter()

@router.post(
    "", 
    tags=["Workspaces"], 
    summary="Create workspace"
)
async def create_workspace(create_workspace_input: CreateWorkspaceInput, request: Request, workspace_type: str = None):
    workspace_name = vars(create_workspace_input)["name"]
    workspace_id = hashlib.md5(workspace_name.encode('utf-8')).hexdigest()
    workspace_type = "private"
    status = requests.post(f"https:///workspaces?type={workspace_type}&id={workspace_id}")
    return status

@router.delete(
    "", 
    tags=["Workspaces"], 
    summary="Delete workspace"
)
async def delete_workspace(create_workspace_input: CreateWorkspaceInput):
    workspace = vars(create_workspace_input)
    if workspace['scope'] not in ['private', 'organization']:
        return "Invalid workspace scope"
    namespace_id = hashlib.md5(workspace["name"].encode('utf-8')).hexdigest()
    namespace = f"workspace-{workspace['scope']}-{namespace_id}"
    status = k8s.delete_namespace(namespace)
    return status