"""Route requests to endpoints"""
from starlette.routing import Route

from .endpoints import NewSecret, TotpCode

URL_ROUTES = [
    Route("/", NewSecret),
    Route("/{secret_id}", TotpCode),
]
