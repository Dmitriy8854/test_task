import uuid
from typing import Union
import time
from random import choice
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio

app = FastAPI()


class ResultResponse(BaseModel):
    result: bool


@app.get("/result")
async def result() -> ResultResponse:
    await asyncio.sleep(20)
    result = choice([True, False])
    print(result)
    return {"result": result}
