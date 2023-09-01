from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from config import settings


class BasicLoginInput(BaseModel):
    email: str = Field(example=settings.DEMO_USER["email"]) 
    password: str = Field(example=settings.DEMO_USER["password"])

