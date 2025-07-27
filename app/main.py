from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

app = FastAPI(title="FortiPipe Sample App")

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fortipipe")

class HealthResponse(BaseModel):
    status: str
    message: str

def get_health_response() -> HealthResponse:
    return HealthResponse(status="ok", message="Service is healthy")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health() -> HealthResponse:
    return get_health_response()

class EchoRequest(BaseModel):
    message: str

class EchoResponse(BaseModel):
    echoed: str

@app.post("/echo", response_model=EchoResponse, tags=["Echo"])
async def echo(data: EchoRequest) -> EchoResponse:
    if not data.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    return EchoResponse(echoed=data.message) 