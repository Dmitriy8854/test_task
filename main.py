import uuid
from typing import Union
import time
from random import choice
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import requests
import json

app = FastAPI()

database = {}


def service_request(query_id: str):
    response = requests.get("http://localhost:8080/result")
    data = json.loads(response.text)
    database[query_id]["result"] = data["result"]


class ResultResponse(BaseModel):
    result: bool | None


class QueryResponse(BaseModel):
    query_id: str


class Query(BaseModel):
    number: str
    latitude: str
    longitude: str


@app.post("/query")
async def query(query: Query, background_tasks: BackgroundTasks) -> QueryResponse:
    query_id = uuid.uuid4()
    database[str(query_id)] = {"result": None, **query.dict()}
    background_tasks.add_task(service_request, str(query_id))
    return {"query_id": str(query_id)}


@app.get("/result")
async def result(query_id: str) -> ResultResponse:
    query = database.get(query_id, None)
    if query is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"result": query["result"]}


@app.get("/ping")
async def ping():
    return "OK"
