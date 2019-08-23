"""Endpoints for Starlette API"""
from base64 import b32encode
from datetime import datetime, timedelta
from uuid import uuid4

import ujson
from aioredis import Redis
from pyotp import TOTP
from pytz import UTC
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response, UJSONResponse


async def connect_redis(request: Request) -> Redis:
    """Get Redis object and ensure connected"""
    redis = request.get("redis")
    if not redis or await redis.ping() != "PONG":
        raise HTTPException(
            503,
            detail="Could not reach database; try again later",
        )
    return redis


class NewSecret(HTTPEndpoint):
    """API Endpoint for creating Tickets"""

    async def post(self, request: Request) -> Response:
        """Create a new Ticket, store in redis"""
        try:
            json_data = ujson.loads(await request.body())
        except ValueError:
            raise HTTPException(
                400,
                detail="Could not unserialize JSON body",
            )

        if "secret" not in json_data:
            raise HTTPException(
                400, detail="Secret not found"
            )

        new_id = str(uuid4())
        expire_at = UTC.localize(
            datetime.now()
        ) + timedelta(seconds=3600)

        redis = await connect_redis(request)
        await redis.set(new_id, json_data["secret"])
        await redis.expireat(new_id, expire_at.timestamp())

        return UJSONResponse(
            {"id": new_id}, status_code=201
        )


class TotpCode(HTTPEndpoint):
    """API Endpoint for fetching individual tickets"""

    interval: int = 30

    async def get(self, request: Request) -> Response:
        """Fetch Ticket identified in URI Path, return data"""
        secret_id = request.path_params["secret_id"]

        redis = await connect_redis(request)
        secret = await redis.get(secret_id)

        if secret is None or secret == "":
            raise HTTPException(
                status_code=404,
                detail="Secret by that ID could not be found.",
            )

        totp = TOTP(
            b32encode(secret.encode("utf8")),
            digits=6,
            interval=self.interval,
        )

        return UJSONResponse({"code": totp.now()})
