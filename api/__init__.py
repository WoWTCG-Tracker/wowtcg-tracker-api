"""
API server for WoWTCG Tracker
"""

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI(title="WoWTCG Tracker API",
  description="API for WoWTCG Tracker")


@app.get("/")
async def get_root() -> dict:
  """
    Root of the API

    Root is set to return "Hello world!"
    """
  return "Hello world!"
