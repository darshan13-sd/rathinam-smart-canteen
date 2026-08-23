import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rathinam_canteen.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="STUDENT") # STUDENT, CANTEEN_OWNER, CLASS_REP, ADMIN
    phone = Column(String(20), nullable=True)
    department = Column(String(50), nullable=True) # e.g. CSE, ECE, IT, MECH, MBA
    roll_number = Column(String(30), nullable=True)
    canteen_id = Column(Integer, ForeignKey("canteens.id"), nullable=True) # For CANTEEN_OWNER
    created_at = Column(DateTime, default=datetime.utcnow)

    canteen = relationship("Canteen", back_populates="owners")
    orders = relationship("Order", back_populates="student")
    announcements = relationship("Announcement", back_populates="author")

class Canteen(Base):
    __tablename__ = "canteens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    token_prefix = Column(String(10), nullable=False, default="C") # e.g. CS, ZC, SY, CCT, JH
    description = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    image_url = Column(String(255), nullable=True)
    is_open = Column(Boolean, default=True)
    active_counters = Column(Integer, default=2)
    avg_prep_time_mins = Column(Integer, default=6)
    parcel_fee = Column(Float, default=10.0)
    parcel_only = Column(Boolean, default=False) # e.g. Seyon parcel rule
    opening_time = Column(String(20), default="08:00 AM")
    closing_time = Column(String(20), default="08:30 PM")
    contact_number = Column(String(20), default="+91 98765 43210")
    created_at = Column(DateTime, default=datetime.utcnow)

    owners = relationship("User", back_populates="canteen")
    menu_items = relationship("MenuItem", back_populates="canteen", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="canteen")
    announcements = relationship("Announcement", back_populates="canteen")

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    canteen_id = Column(Integer, ForeignKey("canteens.id"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50), default="Main Course") # Main Course, Fast Food, Rice, Beverages, Snacks
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    is_veg = Column(Boolean, default=True)
    is_egg = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(String(255), nullable=True)
    prep_time_mins = Column(Integer, default=5)
    parcel_price = Column(Float, default=0.0)
    total_orders_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    canteen = relationship("Canteen", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(30), unique=True, index=True, nullable=False) # e.g. RAT-2026-000101
    token_number = Column(String(20), index=True, nullable=False) # e.g. CS-101
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    canteen_id = Column(Integer, ForeignKey("canteens.id"), nullable=False)
    status = Column(String(30), default="ORDER_PLACED") 
    # ORDER_PLACED, PAYMENT_CONFIRMED, PREPARING, READY_FOR_PICKUP, COMPLETED, CANCELLED
    payment_method = Column(String(20), default="UPI") # UPI, CASH
    payment_status = Column(String(30), default="PAID") # PAID, PAY_AT_COUNTER, PENDING, FAILED
    upi_transaction_id = Column(String(50), nullable=True)
    subtotal = Column(Float, nullable=False, default=0.0)
    parcel_charge = Column(Float, default=0.0)
    is_parcel = Column(Boolean, default=False)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    queue_position = Column(Integer, default=1)
    estimated_wait_time_mins = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ready_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("User", back_populates="orders")
    canteen = relationship("Canteen", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    item_name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    is_parcel = Column(Boolean, default=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author_role = Column(String(20), nullable=False) # CLASS_REP, CANTEEN_OWNER, ADMIN
    author_name = Column(String(100), nullable=False)
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    canteen_id = Column(Integer, ForeignKey("canteens.id"), nullable=True)
    target_class = Column(String(50), nullable=True) # e.g. "ECE-A", "ALL", "CSE-B"
    broadcast_type = Column(String(30), default="CAMPUS") # CAMPUS, CR_BROADCAST, CANTEEN_UPDATE
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="announcements")
    canteen = relationship("Canteen", back_populates="announcements")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
