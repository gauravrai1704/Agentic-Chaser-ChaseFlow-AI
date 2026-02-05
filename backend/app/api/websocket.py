"""
WebSocket Handler for Real-time Updates
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio
from datetime import datetime

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


@router.websocket("/agent-activity")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send simulated agent activity every 3 seconds
            await asyncio.sleep(3)
            
            activity = {
                "type": "agent_activity",
                "data": {
                    "agent_type": "document_chaser",
                    "action": "Sent reminder email",
                    "status": "success",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            await websocket.send_json(activity)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
