from fastapi import FastAPI, APIRouter
from app.routers import authentication
from app.metadata import tags_metadata
from config import settings
import json

app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    contact=settings.PROJECT_CONTACT,
    license_info=settings.PROJECT_LICENSE_INFO,
)

api_router = APIRouter()
api_router.include_router(authentication.router)

app.include_router(api_router)
