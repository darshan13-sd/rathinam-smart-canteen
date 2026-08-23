import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from backend.app.models import Base, engine, get_db
from backend.app.seed_data import seed_database
from backend.app.websocket_manager import ws_manager
from backend.app.routers import (
    auth_routes,
    canteen_routes,
    menu_routes,
    order_routes,
    payment_routes,
    announcement_routes,
    analytics_routes
)

app = FastAPI(
    title="Rathinam College Smart Canteen Hub",
    description="Multi-Canteen Smart Ordering & Crowd Management Platform for Rathinam College",
    version="1.0.0"
)

# CORS middleware for local and web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from starlette.middleware.base import BaseHTTPMiddleware

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheMiddleware)

# Include API Routers
app.include_router(auth_routes.router)
app.include_router(canteen_routes.router)
app.include_router(menu_routes.router)
app.include_router(order_routes.router)
app.include_router(payment_routes.router)
app.include_router(announcement_routes.router)
app.include_router(analytics_routes.router)

# WebSocket endpoint for real-time live ordering & crowd updates
@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int = None,
    canteen_id: int = None
):
    await ws_manager.connect(websocket, user_id, canteen_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Heartbeat or client ping
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, user_id, canteen_id)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_database(db)
    finally:
        db.close()

# Mount static directory for frontend assets and root html
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../static"))
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static_assets")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
