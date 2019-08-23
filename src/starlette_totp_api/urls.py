"""Route requests to endpoints"""
from starlette.routing import Route, WebSocketRoute

from .endpoints import NewSecret, TotpCode
from .sockets import WsTotpCode

URL_ROUTES = [
    Route("/", NewSecret),
    Route("/{secret_id}", TotpCode),
    WebSocketRoute("/ws", WsTotpCode),
]
