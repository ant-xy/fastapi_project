from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.services.middleware_service import limiter
from main import app

@app.middleware("http")
async def add_rate_limit(request: Request, call_next):
    allowed, remaining = limiter.allow(str("ip:"+request.client.host))

    if allowed:
        response = await call_next(request)
        return response
    
    return JSONResponse(content={"status": 429, "message":"You have been ratelimited."})


