from sqlalchemy.orm import Session
from backend.app.models import Order, Canteen, MenuItem
from backend.app.schemas import CanteenCrowdInfo

def calculate_canteen_crowd(canteen: Canteen, db: Session) -> CanteenCrowdInfo:
    active_statuses = ["ORDER_PLACED", "PAYMENT_CONFIRMED", "PREPARING"]
    
    # Active orders for this canteen
    active_orders_list = db.query(Order).filter(
        Order.canteen_id == canteen.id,
        Order.status.in_(active_statuses)
    ).all()
    
    active_orders = len(active_orders_list)
    preparing_orders = sum(1 for o in active_orders_list if o.status == "PREPARING")
    waiting_students = sum(1 for o in active_orders_list if o.status in ["ORDER_PLACED", "PAYMENT_CONFIRMED"])
    
    counters = max(1, canteen.active_counters or 1)
    avg_prep = canteen.avg_prep_time_mins or 5
    
    if not canteen.is_open:
        est_wait = 0
        crowd_level = "CLOSED"
    elif active_orders == 0:
        est_wait = avg_prep
        crowd_level = "LOW"
    else:
        # Dynamic queue calculation formula
        raw_wait = (active_orders * avg_prep) / counters
        est_wait = max(3, int(round(raw_wait)))
        
        if est_wait <= 10:
            crowd_level = "LOW"
        elif est_wait <= 20:
            crowd_level = "MEDIUM"
        else:
            crowd_level = "HIGH"
            
    return CanteenCrowdInfo(
        canteen_id=canteen.id,
        canteen_name=canteen.name,
        active_orders=active_orders,
        preparing_orders=preparing_orders,
        waiting_students=waiting_students,
        active_counters=counters,
        avg_prep_time_mins=avg_prep,
        estimated_wait_time_mins=est_wait,
        crowd_level=crowd_level,
        is_open=canteen.is_open
    )

def calculate_order_queue_position(order_id: int, canteen_id: int, db: Session) -> tuple[int, int]:
    """Returns (queue_position, estimated_wait_mins)"""
    canteen = db.query(Canteen).filter(Canteen.id == canteen_id).first()
    if not canteen:
        return 1, 10
        
    active_orders = db.query(Order).filter(
        Order.canteen_id == canteen_id,
        Order.status.in_(["ORDER_PLACED", "PAYMENT_CONFIRMED", "PREPARING"])
    ).order_by(Order.id.asc()).all()
    
    pos = 1
    for idx, ord_obj in enumerate(active_orders, start=1):
        if ord_obj.id == order_id:
            pos = idx
            break
            
    counters = max(1, canteen.active_counters or 1)
    avg_prep = canteen.avg_prep_time_mins or 5
    est_wait = max(3, int(round((pos * avg_prep) / counters)))
    
    return pos, est_wait
