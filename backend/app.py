# from api.services import networkservices
from api.v1.network import router as network_router
from fastapi import FastAPI

app = FastAPI(title="WinSecure")
app.include_router(network_router, prefix="/api/v1/network")


@app.get("/api/v1/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
