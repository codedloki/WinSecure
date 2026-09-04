# from api.services import networkservices
from backend.api.v1.network import router as network_router
from backend.api.v1.systemroutes import router as systemrouter
from fastapi import FastAPI

app = FastAPI(title="WinSecure")
app.include_router(network_router, prefix="/api/v1/network")
app.include_router(systemrouter,prefix="/api/v1/system")

@app.get("/api/v1/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
