import json
import os
import asyncio
from typing import List, Dict, Union, Any, Optional
from urllib.parse import unquote_plus
from dateutil.parser import parse
from dotenv import load_dotenv
from fastapi import FastAPI, Response, HTTPException, Body, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import motor.motor_asyncio
from bson.objectid import ObjectId

# --------------- Constants --------------------
load_dotenv()
MONGOURI = os.getenv("MONGOURI")

# --------------- FastAPI Setup -----------------
app = FastAPI()

# Allowed origins for CORS
origins = [
    "http://localhost:3000",  # Allow frontend to connect
    # Add other origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------- MongoDB Setup ------------------
db = motor.motor_asyncio.AsyncIOMotorClient(MONGOURI).dev_print_data

# --------------- Utility Functions --------------

def raise_error(response: Dict, status_code: int = 400) -> Response:
    """
    Creates and returns an error response.

    Parameters:
    - response (dict): The content of the response.
    - status_code (int, optional): The HTTP status code. Defaults to 400.

    Returns:
    - Response: A FastAPI Response object.
    """
    assert status_code >= 400 and status_code < 500, "Status code must be between 400 and 500"
    assert type(response) == dict, "Response must be a dictionary"

    json_str = json.dumps(response, indent=4, default=str)
    return Response(content=json_str, media_type='application/json', status_code=status_code)

def give_response(response: Dict, status_code: int = 200) -> Response:
    """
    Creates and returns a success response.

    Parameters:
    - response (dict): The content of the response.
    - status_code (int, optional): The HTTP status code. Defaults to 200.

    Returns:
    - Response: A FastAPI Response object.
    """
    assert status_code >= 200 and status_code < 300, "Status code must be between 200 and 300"
    assert type(response) == dict, "Response must be a dictionary"

    json_str = json.dumps(response, indent=4, default=str)
    return Response(content=json_str, media_type='application/json', status_code=status_code)

# --------------- FastAPI Endpoints --------------

@app.get("/data/")
async def get_data() -> Dict:
    """
    Fetches all the data from the database.

    Returns:
    - dict: A dictionary containing the fetched data.
    """
    projects = await db.print_data.find().to_list(None)
    return give_response({"response": projects}, 200)
