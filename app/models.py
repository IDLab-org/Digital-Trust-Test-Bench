from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from config import settings


class BasicLoginInput(BaseModel):
    username: str = Field(example="demo.user")
    password: str = Field(example="password123")

