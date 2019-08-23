"""Starlette Application"""
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import (
    TrustedHostMiddleware,
)
from starlette.responses import JSONResponse

from .config import ALLOWED_HOSTS, DEBUG, REDIS_URL, TESTING
from .middleware.redis import RedisMiddleware
from .urls import URL_ROUTES

app = Starlette(debug=DEBUG, routes=URL_ROUTES)

app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["GET", "HEAD", "OPTIONS", "POST"],
    allow_origins=["*"],
)

if not DEBUG:
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS
    )

if not TESTING:
    app.add_middleware(RedisMiddleware, redis_url=REDIS_URL)


@app.exception_handler(HTTPException)
async def http_exception(request, exc):
    """General Handler for HTTP Exceptions"""
    return JSONResponse(
        {"message": exc.detail}, status_code=exc.status_code
    )
