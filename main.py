from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router

app = FastAPI()

app.include_router(router, prefix="/api")

# Mount after API routes
app.mount("/", StaticFiles(directory="static", html=True), name="static")
