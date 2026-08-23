from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.models import MenuItem, Canteen, User, get_db
from backend.app.schemas import MenuItemResponse, MenuItemCreate, MenuItemUpdate
from backend.app.auth import require_auth, require_role
from backend.app.websocket_manager import ws_manager

router = APIRouter(prefix="/api/menu", tags=["Menu"])

@router.get("", response_model=List[MenuItemResponse])
def get_menu(
    canteen_id: Optional[int] = None,
    category: Optional[str] = None,
    is_veg: Optional[bool] = None,
    available_only: Optional[bool] = False,
    db: Session = Depends(get_db)
):
    query = db.query(MenuItem)
    if canteen_id:
        query = query.filter(MenuItem.canteen_id == canteen_id)
    if category:
        query = query.filter(MenuItem.category == category)
    if is_veg is not None:
        query = query.filter(MenuItem.is_veg == is_veg)
    if available_only:
        query = query.filter(MenuItem.is_available == True)
    return query.all()

@router.get("/search")
def search_food(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """
    Search dish across all college canteens and return comparison cards with
    price, availability, and canteen waiting time.
    """
    from backend.app.crowd_engine import calculate_canteen_crowd
    term = f"%{query.lower()}%"
    items = db.query(MenuItem).filter(MenuItem.name.ilike(term)).all()
    
    results = []
    for item in items:
        canteen = db.query(Canteen).filter(Canteen.id == item.canteen_id).first()
        if canteen:
            crowd = calculate_canteen_crowd(canteen, db)
            results.append({
                "item_id": item.id,
                "name": item.name,
                "category": item.category,
                "description": item.description,
                "price": item.price,
                "is_veg": item.is_veg,
                "is_egg": item.is_egg,
                "is_available": item.is_available,
                "image_url": item.image_url,
                "canteen_id": canteen.id,
                "canteen_name": canteen.name,
                "canteen_location": canteen.location,
                "crowd_level": crowd.crowd_level,
                "estimated_wait_mins": crowd.estimated_wait_time_mins,
                "is_canteen_open": canteen.is_open
            })
    return results

@router.post("", response_model=MenuItemResponse)
async def create_menu_item(
    payload: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN", "CANTEEN_OWNER"]))
):
    if current_user.role == "CANTEEN_OWNER" and current_user.canteen_id != payload.canteen_id:
        raise HTTPException(status_code=403, detail="Cannot add items to another canteen")
        
    item = MenuItem(**payload.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    
    await ws_manager.broadcast_event("menu_item_created", {
        "canteen_id": item.canteen_id,
        "item_id": item.id,
        "name": item.name,
        "price": item.price,
        "is_available": item.is_available
    })
    return item

@router.put("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    payload: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN", "CANTEEN_OWNER"]))
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    if current_user.role == "CANTEEN_OWNER" and current_user.canteen_id != item.canteen_id:
        raise HTTPException(status_code=403, detail="Cannot edit items from another canteen")
        
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(item, k, v)
        
    db.commit()
    db.refresh(item)
    
    await ws_manager.broadcast_event("menu_item_updated", {
        "canteen_id": item.canteen_id,
        "item_id": item.id,
        "name": item.name,
        "price": item.price,
        "is_available": item.is_available
    })
    return item

@router.post("/{item_id}/toggle-availability")
async def toggle_availability(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN", "CANTEEN_OWNER"]))
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    if current_user.role == "CANTEEN_OWNER" and current_user.canteen_id != item.canteen_id:
        raise HTTPException(status_code=403, detail="Cannot edit items from another canteen")
        
    item.is_available = not item.is_available
    db.commit()
    db.refresh(item)
    
    # Broadcast to all connected student clients in real time
    await ws_manager.broadcast_event("item_availability_changed", {
        "item_id": item.id,
        "canteen_id": item.canteen_id,
        "name": item.name,
        "is_available": item.is_available
    })
    
    status_label = "Available" if item.is_available else "Out of Stock"
    return {"message": f"{item.name} is now {status_label}", "item_id": item.id, "is_available": item.is_available}

@router.delete("/{item_id}")
async def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN", "CANTEEN_OWNER"]))
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    if current_user.role == "CANTEEN_OWNER" and current_user.canteen_id != item.canteen_id:
        raise HTTPException(status_code=403, detail="Cannot delete items from another canteen")
        
    canteen_id = item.canteen_id
    db.delete(item)
    db.commit()
    
    await ws_manager.broadcast_event("menu_item_deleted", {"item_id": item_id, "canteen_id": canteen_id})
    return {"message": "Menu item deleted successfully"}
