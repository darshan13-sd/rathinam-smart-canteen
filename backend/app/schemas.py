from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: str
    phone: Optional[str] = None
    department: Optional[str] = None
    roll_number: Optional[str] = None
    canteen_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class MenuItemBase(BaseModel):
    name: str
    category: Optional[str] = "Main Course"
    description: Optional[str] = None
    price: float
    is_veg: bool = True
    is_egg: bool = False
    is_available: bool = True
    image_url: Optional[str] = None
    prep_time_mins: int = 5
    parcel_price: float = 0.0

class MenuItemCreate(MenuItemBase):
    canteen_id: int

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_veg: Optional[bool] = None
    is_egg: Optional[bool] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None
    prep_time_mins: Optional[int] = None
    parcel_price: Optional[float] = None

class MenuItemResponse(MenuItemBase):
    id: int
    canteen_id: int
    total_orders_count: int
    created_at: datetime
    class Config:
        from_attributes = True

class CanteenBase(BaseModel):
    name: str
    slug: str
    token_prefix: str
    description: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    is_open: bool = True
    active_counters: int = 2
    avg_prep_time_mins: int = 6
    parcel_fee: float = 10.0
    parcel_only: bool = False
    opening_time: str = "08:00 AM"
    closing_time: str = "08:30 PM"
    contact_number: str = "+91 98765 43210"

class CanteenCreate(CanteenBase):
    pass

class CanteenCrowdInfo(BaseModel):
    canteen_id: int
    canteen_name: str
    active_orders: int
    preparing_orders: int
    waiting_students: int
    active_counters: int
    avg_prep_time_mins: int
    estimated_wait_time_mins: int
    crowd_level: str # LOW, MEDIUM, HIGH
    is_open: bool

class CanteenResponse(CanteenBase):
    id: int
    created_at: datetime
    crowd_info: Optional[CanteenCrowdInfo] = None
    menu_items: List[MenuItemResponse] = []
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1
    is_parcel: bool = False

class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    item_name: str
    quantity: int
    unit_price: float
    subtotal: float
    is_parcel: bool = False
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    canteen_id: int
    items: List[OrderItemCreate]
    payment_method: str = "UPI" # UPI, CASH
    is_parcel: bool = False
    notes: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: str # ORDER_PLACED, PAYMENT_CONFIRMED, PREPARING, READY_FOR_PICKUP, COMPLETED, CANCELLED
    payment_status: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    order_number: str
    token_number: str
    student_id: int
    student_name: Optional[str] = None
    canteen_id: int
    canteen_name: Optional[str] = None
    status: str
    payment_method: str
    payment_status: str
    upi_transaction_id: Optional[str] = None
    subtotal: float
    parcel_charge: float
    is_parcel: bool
    total_amount: float
    notes: Optional[str] = None
    queue_position: int
    estimated_wait_time_mins: int
    created_at: datetime
    updated_at: datetime
    ready_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []
    class Config:
        from_attributes = True

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    canteen_id: Optional[int] = None
    target_class: Optional[str] = "ALL"
    broadcast_type: str = "CAMPUS" # CAMPUS, CR_BROADCAST, CANTEEN_UPDATE

class AnnouncementResponse(BaseModel):
    id: int
    author_id: int
    author_role: str
    author_name: str
    title: str
    content: str
    canteen_id: Optional[int] = None
    canteen_name: Optional[str] = None
    target_class: Optional[str] = None
    broadcast_type: str
    is_active: bool
    created_at: datetime
    whatsapp_share_url: Optional[str] = None
    class Config:
        from_attributes = True

class MockUPIPaymentRequest(BaseModel):
    order_id: int
    upi_id: str
    app: str = "GPay" # GPay, PhonePe, Paytm, BHIM

class MockUPIPaymentResponse(BaseModel):
    success: bool
    transaction_id: str
    status: str
    message: str
    order_id: int
    token_number: str
