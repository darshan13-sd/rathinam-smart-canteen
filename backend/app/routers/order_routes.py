from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import random
from backend.app.models import Order, OrderItem, MenuItem, Canteen, User, get_db
from backend.app.schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from backend.app.auth import require_auth, get_current_user
from backend.app.crowd_engine import calculate_order_queue_position, calculate_canteen_crowd
from backend.app.websocket_manager import ws_manager

router = APIRouter(prefix="/api/orders", tags=["Orders"])

def serialize_order(order: Order, db: Session) -> dict:
    student = db.query(User).filter(User.id == order.student_id).first()
    canteen = db.query(Canteen).filter(Canteen.id == order.canteen_id).first()
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return {
        "id": order.id,
        "order_number": order.order_number,
        "token_number": order.token_number,
        "student_id": order.student_id,
        "student_name": student.full_name if student else "Student",
        "canteen_id": order.canteen_id,
        "canteen_name": canteen.name if canteen else "Canteen",
        "status": order.status,
        "payment_method": order.payment_method,
        "payment_status": order.payment_status,
        "upi_transaction_id": order.upi_transaction_id,
        "subtotal": order.subtotal,
        "parcel_charge": order.parcel_charge,
        "is_parcel": order.is_parcel,
        "total_amount": order.total_amount,
        "notes": order.notes,
        "queue_position": order.queue_position,
        "estimated_wait_time_mins": order.estimated_wait_time_mins,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "ready_at": order.ready_at,
        "completed_at": order.completed_at,
        "items": [
            {
                "id": it.id,
                "menu_item_id": it.menu_item_id,
                "item_name": it.item_name,
                "quantity": it.quantity,
                "unit_price": it.unit_price,
                "subtotal": it.subtotal,
                "is_parcel": it.is_parcel
            } for it in items
        ]
    }

@router.post("", response_model=OrderResponse)
async def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    canteen = db.query(Canteen).filter(Canteen.id == payload.canteen_id).first()
    if not canteen:
        raise HTTPException(status_code=404, detail="Canteen not found")
        
    if not canteen.is_open:
        raise HTTPException(status_code=400, detail=f"{canteen.name} is currently closed.")
        
    if not payload.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
        
    subtotal = 0.0
    parcel_charge = 0.0
    order_items_to_create = []
    
    for cart_item in payload.items:
        menu_item = db.query(MenuItem).filter(
            MenuItem.id == cart_item.menu_item_id,
            MenuItem.canteen_id == canteen.id
        ).first()
        
        if not menu_item:
            raise HTTPException(status_code=400, detail=f"Item ID {cart_item.menu_item_id} does not belong to {canteen.name}")
            
        if not menu_item.is_available:
            raise HTTPException(status_code=400, detail=f"'{menu_item.name}' is currently Out of Stock!")
            
        if cart_item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Invalid item quantity")
            
        line_total = menu_item.price * cart_item.quantity
        subtotal += line_total
        
        # Track order popularity count
        menu_item.total_orders_count += cart_item.quantity
        
        # Per-item parcel calculation
        item_is_parcel = (cart_item.is_parcel or payload.is_parcel or canteen.parcel_only)
        if item_is_parcel:
            parcel_charge += (canteen.parcel_fee * cart_item.quantity)
        
        order_items_to_create.append({
            "menu_item_id": menu_item.id,
            "item_name": menu_item.name,
            "quantity": cart_item.quantity,
            "unit_price": menu_item.price,
            "subtotal": line_total,
            "is_parcel": item_is_parcel
        })

    has_any_parcel = any(item["is_parcel"] for item in order_items_to_create)
    total_amount = subtotal + parcel_charge
    
    # Generate sequential or unique Token and Order IDs
    order_count_today = db.query(Order).filter(Order.canteen_id == canteen.id).count() + 101
    token_num = f"{canteen.token_prefix}-{order_count_today}"
    order_num = f"RAT-2026-{random.randint(100000, 999999)}"
    
    payment_status = "PAID" if payload.payment_method == "UPI" else "PAY_AT_COUNTER"
    initial_status = "PAYMENT_CONFIRMED" if payload.payment_method == "UPI" else "ORDER_PLACED"
    
    order = Order(
        order_number=order_num,
        token_number=token_num,
        student_id=current_user.id,
        canteen_id=canteen.id,
        status=initial_status,
        payment_method=payload.payment_method,
        payment_status=payment_status,
        upi_transaction_id=f"UPI-RAT-{random.randint(10000, 99999)}" if payload.payment_method == "UPI" else None,
        subtotal=subtotal,
        parcel_charge=parcel_charge,
        is_parcel=has_any_parcel,
        total_amount=total_amount,
        notes=payload.notes
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    for it_data in order_items_to_create:
        oi = OrderItem(order_id=order.id, **it_data)
        db.add(oi)
    db.commit()
    
    # Calculate queue position & wait time
    pos, est_wait = calculate_order_queue_position(order.id, canteen.id, db)
    order.queue_position = pos
    order.estimated_wait_time_mins = est_wait
    db.commit()
    db.refresh(order)
    
    serialized = serialize_order(order, db)
    
    # Broadcast order to canteen owner & campus crowd updates
    crowd_info = calculate_canteen_crowd(canteen, db)
    await ws_manager.send_canteen_event(canteen.id, "new_order", serialized)
    await ws_manager.broadcast_event("crowd_update", crowd_info.dict())
    
    return serialized

@router.get("/user/my-orders", response_model=List[OrderResponse])
def get_my_orders(db: Session = Depends(get_db), current_user: User = Depends(require_auth)):
    orders = db.query(Order).filter(Order.student_id == current_user.id).order_by(Order.created_at.desc()).all()
    return [serialize_order(o, db) for o in orders]

@router.get("/canteen/{canteen_id}", response_model=List[OrderResponse])
def get_canteen_orders(canteen_id: int, status_filter: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Order).filter(Order.canteen_id == canteen_id)
    if status_filter and status_filter != "ALL":
        query = query.filter(Order.status == status_filter)
    orders = query.order_by(Order.created_at.desc()).all()
    return [serialize_order(o, db) for o in orders]

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return serialize_order(order, db)

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    old_status = order.status
    order.status = payload.status
    
    if payload.payment_status:
        order.payment_status = payload.payment_status
        
    if payload.status == "READY_FOR_PICKUP":
        order.ready_at = datetime.utcnow()
    elif payload.status == "COMPLETED":
        order.completed_at = datetime.utcnow()
        if order.payment_status == "PAY_AT_COUNTER":
            order.payment_status = "PAID"
            
    db.commit()
    db.refresh(order)
    
    # Recalculate queue positions
    pos, est_wait = calculate_order_queue_position(order.id, order.canteen_id, db)
    order.queue_position = pos
    order.estimated_wait_time_mins = est_wait if order.status not in ["READY_FOR_PICKUP", "COMPLETED"] else 0
    db.commit()
    
    serialized = serialize_order(order, db)
    canteen = db.query(Canteen).filter(Canteen.id == order.canteen_id).first()
    crowd_info = calculate_canteen_crowd(canteen, db)
    
    # Broadcast to user and canteen
    await ws_manager.send_user_event(order.student_id, "order_status_updated", serialized)
    await ws_manager.send_canteen_event(order.canteen_id, "order_status_updated", serialized)
    await ws_manager.broadcast_event("crowd_update", crowd_info.dict())
    
    return {
        "message": f"Order {order.token_number} status updated to {order.status}",
        "order": serialized
    }
