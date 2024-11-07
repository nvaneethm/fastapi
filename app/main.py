# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import QueryRequest
from app.core.gpt_service import generate_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/query/")
async def get_gpt_response(request: QueryRequest):
    user_query = request.user_query
    response = generate_response(user_query)
    return {"response": response}
