# models.py

from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    user_query: str

class JiraTicket(BaseModel):
    id: str
    summary: str
    description: str
    status: str
