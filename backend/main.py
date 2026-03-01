from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import router as api_router
from backend.ws import router as ws_router

app = FastAPI(title="GhostWire Agent") #this is our main FastAPI application for the ghostwire agent

# Allow frontend on port 3000 to call backend on port 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(ws_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the GhostWire Agent API!"}