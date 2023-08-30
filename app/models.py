from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from config import settings


class BasicLoginInput(BaseModel):
    email: str = Field(example="user@abc.com")
    password: str = Field(example="password123")

