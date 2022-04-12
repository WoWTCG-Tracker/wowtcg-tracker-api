"""API server for WoWTCG Tracker"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI()


@app.get("/")
async def read_root():
    """
    Root of the API

    Root is set to return "Hello world!" string.
    """
    return "Hello world!"
