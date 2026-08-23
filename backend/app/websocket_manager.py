import json
from typing import List, Dict, Any
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[int, List[WebSocket]] = {}
        self.canteen_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int = None, canteen_id: int = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)
            
        if canteen_id:
            if canteen_id not in self.canteen_connections:
                self.canteen_connections[canteen_id] = []
            self.canteen_connections[canteen_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int = None, canteen_id: int = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
                
        if canteen_id and canteen_id in self.canteen_connections:
            if websocket in self.canteen_connections[canteen_id]:
                self.canteen_connections[canteen_id].remove(websocket)

    async def broadcast_event(self, event_type: str, data: Any):
        """Broadcasts event to all active clients (students, owners, CRs, admins)"""
        message = json.dumps({"type": event_type, "data": data}, default=str)
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

    async def send_user_event(self, user_id: int, event_type: str, data: Any):
        """Sends targeted event to specific user (e.g. order ready notification)"""
        message = json.dumps({"type": event_type, "data": data}, default=str)
        if user_id in self.user_connections:
            for connection in list(self.user_connections[user_id]):
                try:
                    await connection.send_text(message)
                except Exception:
                    pass

    async def send_canteen_event(self, canteen_id: int, event_type: str, data: Any):
        """Sends targeted event to specific canteen owner portal"""
        message = json.dumps({"type": event_type, "data": data}, default=str)
        if canteen_id in self.canteen_connections:
            for connection in list(self.canteen_connections[canteen_id]):
                try:
                    await connection.send_text(message)
                except Exception:
                    pass

ws_manager = ConnectionManager()
