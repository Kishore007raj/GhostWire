#main Web socket server for the ghostwire agent, responsible for receiving data from the agent and sending it to the frontend

from fastapi import WebSocket, APIRouter
import asyncio
from backend.db import fetch_all_alerts

router = APIRouter() #this is for handling WebSocket connections for the ghostwire agent

#this is for handling WebSocket connections from the agent and sending alerts to the frontend

@router.websocket("/live")
async def live_alerts(websocket: WebSocket):
    await websocket.accept()

    last_seen_id = 0

    try:
        while True:
            alerts = fetch_all_alerts(limit=100)

            new_alerts = [
                alert for alert in alerts
                if alert["id"] > last_seen_id
            ]

            for alert in reversed(new_alerts):
                await websocket.send_json(alert)
                last_seen_id = alert["id"]

            await asyncio.sleep(2)
    except Exception as e:
        # likely a WebSocketDisconnect or other send error
        print(f"WebSocket connection closed or error: {e}")
    finally:
        try:
            await websocket.close()
        except Exception:
            pass