from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import random
from backend.app.models import Order, get_db
from backend.app.schemas import MockUPIPaymentRequest, MockUPIPaymentResponse
from backend.app.websocket_manager import ws_manager

router = APIRouter(prefix="/api/payments", tags=["Payments"])

@router.post("/verify-mock-upi", response_model=MockUPIPaymentResponse)
async def verify_mock_upi(payload: MockUPIPaymentRequest, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == payload.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    txn_id = f"UPI-{payload.app.upper()}-{random.randint(100000, 999999)}"
    order.payment_method = "UPI"
    order.payment_status = "PAID"
    order.upi_transaction_id = txn_id
    if order.status == "ORDER_PLACED":
        order.status = "PAYMENT_CONFIRMED"
        
    db.commit()
    db.refresh(order)
    
    await ws_manager.send_user_event(order.student_id, "payment_success", {
        "order_id": order.id,
        "token_number": order.token_number,
        "transaction_id": txn_id,
        "amount": order.total_amount
    })
    
    return MockUPIPaymentResponse(
        success=True,
        transaction_id=txn_id,
        status="SUCCESS",
        message="UPI Payment confirmed successfully!",
        order_id=order.id,
        token_number=order.token_number
    )
