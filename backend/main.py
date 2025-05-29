from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pathlib

app = FastAPI()

# Path to the frontend build directory
frontend_build = pathlib.Path(__file__).resolve().parents[1] / "frontend" / "build"

app.mount("/", StaticFiles(directory=frontend_build, html=True), name="static")
