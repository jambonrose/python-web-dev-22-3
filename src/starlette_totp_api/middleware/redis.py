"""Middleware for interacting with Redis"""
from typing import Union

import attr
from aioredis import Redis, create_redis_pool
from attr.validators import instance_of
from starlette.datastructures import URL
from starlette.middleware.lifespan import LifespanHandler
from starlette.types import ASGIApp, ASGIInstance, Scope

ATTR_NAME = "redis"


@attr.s(auto_attribs=True)
class RedisMiddleware:
    """Inject Redis connection into Requests for Endpoints"""

    app: ASGIApp
    redis_url: Union[str, URL]
    _redis: Redis = attr.ib(
        init=False, validator=instance_of(Redis)
    )

    def __call__(self, scope: Scope) -> ASGIInstance:
        """Inject Redis into Scope"""
        if scope["type"] == "lifespan":
            return LifespanHandler(
                self.app,
                scope,
                [self.startup],
                [self.shutdown],
            )
        scope[ATTR_NAME] = self._redis
        return self.app(scope)

    async def startup(self) -> None:
        """Connect to Redis on app Startup"""
        self._redis = await create_redis_pool(
            str(self.redis_url), encoding="utf8"
        )

    async def shutdown(self) -> None:
        """Close Redis connections on app exit"""
        self._redis.close()
