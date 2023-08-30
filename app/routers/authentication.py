from fastapi import APIRouter, Body, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from config import settings
from app.models import *
import json

router = APIRouter()

@router.post(
    "/login", 
    tags=["Authentication"], 
    summary="Basic login"
)
async def basic_login(basic_login_input: BasicLoginInput):
    email = vars(basic_login_input)["email"]
    password = vars(basic_login_input)["password"]
    if (username, password) == \
        (settings.DEMO_USER["username"], settings.DEMO_USER["password"]):
            return True
    return False