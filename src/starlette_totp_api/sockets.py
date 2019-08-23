"""Demonstrate websocket usage in Starlette"""
from starlette.endpoints import WebSocketEndpoint


class WsTotpCode(WebSocketEndpoint):
    """Websocket to echo back received text"""

    encoding = "text"

    async def on_receive(self, websocket, data):
        """Echo data back on receipt"""
        await websocket.send_text(
            f"Message text was: {data}"
        )
