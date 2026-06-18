from fastapi import WebSocket
from typing import List
import logging

# Configure logger
logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []
        logger.info("ConnectionManager initialized")

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket) -> None:
        try:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total connections: {len(self.active_connections)}")
        except ValueError:
            logger.warning("Attempted to disconnect a websocket that was not in active connections")

    async def broadcast(self, message: str) -> None:
        """
        Broadcast message to all active connections.
        Failed connections are automatically removed to prevent breaking broadcasts.
        """
        if not self.active_connections:
            logger.debug("No active connections to broadcast to")
            return

        failed_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send message to WebSocket connection: {e}", exc_info=True)
                failed_connections.append(connection)

        # Remove failed connections
        for connection in failed_connections:
            try:
                self.active_connections.remove(connection)
                logger.warning(f"Removed failed WebSocket connection. Remaining connections: {len(self.active_connections)}")
            except ValueError:
                pass

        if failed_connections:
            logger.info(f"Broadcast completed with {len(failed_connections)} failed connection(s)")
        else:
            logger.debug(f"Message successfully broadcasted to {len(self.active_connections)} connection(s)")


# Create a single instance to be used across the application
manager = ConnectionManager()