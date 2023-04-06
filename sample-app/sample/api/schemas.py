from datetime import date
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    phone: str
    email: str
    name: str