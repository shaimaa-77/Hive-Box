
from fastapi import FastAPI
from fastapi import APIRouter
import requests
from constants import OPEN_SENSE_API_URL
import sys
import toml

def get_app_version():
    try:
        with open("pyproject.toml","r",encoding="utf-8") as file:
            config=toml.load(file)
        app_version=config.get("tool",{}).get(
            "poetry",{}).get("version","unknown version")
        return app_version
    except FileNotFoundError:
        return "pyproject.toml not found"
app = FastAPI(
    title="Hive Box",
    description="Hive Box project",
    version=get_app_version(),
)
@app.get("/version")
async def get_version():
    return {"version": get_app_version()}