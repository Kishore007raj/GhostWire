from fastapi import FastAPI
from backend.api import router as api_router
from backend.ws import router as ws_router

app = FastAPI(title="GhostWire Agent") #this is our main FastAPI application for the ghostwire agent

app.include_router(api_router)
app.include_router(ws_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the GhostWire Agent API!"}