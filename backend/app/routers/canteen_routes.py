from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.models import Canteen, MenuItem, User, get_db
from backend.app.schemas import CanteenResponse, CanteenCreate, CanteenCrowdInfo
from backend.app.crowd_engine import calculate_canteen_crowd
from backend.app.auth import require_auth, require_role
from backend.app.websocket_manager import ws_manager

router = APIRouter(prefix="/api/canteens", tags=["Canteens"])

@router.get("", response_model=List[CanteenResponse])
def list_canteens(db: Session = Depends(get_db)):
    canteens = db.query(Canteen).all()
    results = []
    for c in canteens:
        crowd = calculate_canteen_crowd(c, db)
        items = db.query(MenuItem).filter(MenuItem.canteen_id == c.id).all()
        c_dict = {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "token_prefix": c.token_prefix,
            "description": c.description,
            "location": c.location,
            "image_url": c.image_url,
            "is_open": c.is_open,
            "active_counters": c.active_counters,
            "avg_prep_time_mins": c.avg_prep_time_mins,
            "parcel_fee": c.parcel_fee,
            "parcel_only": c.parcel_only,
            "opening_time": c.opening_time,
            "closing_time": c.closing_time,
            "contact_number": c.contact_number,
            "created_at": c.created_at,
            "crowd_info": crowd,
            "menu_items": items
        }
        results.append(c_dict)
    return results

@router.get("/{canteen_id}", response_model=CanteenResponse)
def get_canteen(canteen_id: int, db: Session = Depends(get_db)):
    c = db.query(Canteen).filter(Canteen.id == canteen_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Canteen not found")
    crowd = calculate_canteen_crowd(c, db)
    items = db.query(MenuItem).filter(MenuItem.canteen_id == c.id).all()
    return {
        "id": c.id,
        "name": c.name,
        "slug": c.slug,
        "token_prefix": c.token_prefix,
        "description": c.description,
        "location": c.location,
        "image_url": c.image_url,
        "is_open": c.is_open,
        "active_counters": c.active_counters,
        "avg_prep_time_mins": c.avg_prep_time_mins,
        "parcel_fee": c.parcel_fee,
        "parcel_only": c.parcel_only,
        "opening_time": c.opening_time,
        "closing_time": c.closing_time,
        "contact_number": c.contact_number,
        "created_at": c.created_at,
        "crowd_info": crowd,
        "menu_items": items
    }

@router.get("/{canteen_id}/crowd", response_model=CanteenCrowdInfo)
def get_canteen_crowd(canteen_id: int, db: Session = Depends(get_db)):
    c = db.query(Canteen).filter(Canteen.id == canteen_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Canteen not found")
    return calculate_canteen_crowd(c, db)

@router.post("", response_model=CanteenResponse)
def create_canteen(payload: CanteenCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(["ADMIN"]))):
    canteen = Canteen(**payload.dict())
    db.add(canteen)
    db.commit()
    db.refresh(canteen)
    crowd = calculate_canteen_crowd(canteen, db)
    return {
        "id": canteen.id,
        "name": canteen.name,
        "slug": canteen.slug,
        "token_prefix": canteen.token_prefix,
        "description": canteen.description,
        "location": canteen.location,
        "image_url": canteen.image_url,
        "is_open": canteen.is_open,
        "active_counters": canteen.active_counters,
        "avg_prep_time_mins": canteen.avg_prep_time_mins,
        "parcel_fee": canteen.parcel_fee,
        "parcel_only": canteen.parcel_only,
        "opening_time": canteen.opening_time,
        "closing_time": canteen.closing_time,
        "contact_number": canteen.contact_number,
        "created_at": canteen.created_at,
        "crowd_info": crowd,
        "menu_items": []
    }

@router.put("/{canteen_id}/status")
async def update_canteen_status(
    canteen_id: int, 
    is_open: bool = None, 
    active_counters: int = None, 
    payload: dict = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN", "CANTEEN_OWNER"]))
):
    c = db.query(Canteen).filter(Canteen.id == canteen_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Canteen not found")
    if current_user.role == "CANTEEN_OWNER" and current_user.canteen_id != canteen_id:
        raise HTTPException(status_code=403, detail="Cannot manage another canteen")
    
    if payload and "is_open" in payload:
        c.is_open = bool(payload["is_open"])
    elif is_open is not None:
        c.is_open = is_open

    if payload and "active_counters" in payload:
        c.active_counters = int(payload["active_counters"])
    elif active_counters is not None:
        c.active_counters = active_counters

    db.commit()
    
    crowd = calculate_canteen_crowd(c, db)
    await ws_manager.broadcast_event("canteen_status_update", {
        "canteen_id": c.id,
        "is_open": c.is_open,
        "active_counters": c.active_counters,
        "crowd_info": crowd.dict()
    })
    return {"message": "Canteen status updated", "canteen_id": c.id, "is_open": c.is_open}
