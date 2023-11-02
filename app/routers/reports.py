from fastapi import APIRouter
from config import settings
from jinja2 import Environment, PackageLoader
from app.models import *
from app.controllers import k8s
import yaml, json, requests, textwrap

router = APIRouter()

@router.get(
    "/render", 
    tags=["Reports"], 
    summary=""
)
async def render_project(project_id: str, workspace_id: str):
    # r = requests.get(f"http://localhost:5050/allure-docker-service/emailable-report/render?project_id={project_id}")
    # This will only work incluster, for localhost, you need to port forward this service and access through localhost
    r = requests.get(f"http://allure.{workspace_id}:5050/allure-docker-service/emailable-report/render?project_id={project_id}")
    r = r.text
    r = r.replace("\n", "")
    r = r.replace("\\", "")
    return r