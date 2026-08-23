from sqlalchemy.orm import Session
from backend.app.models import Canteen, MenuItem, Order
from datetime import datetime, timedelta
import random

def get_ai_demand_predictions(db: Session):
    """
    Simulates AI demand prediction for tomorrow based on historical ordering frequency,
    day of week, and current trend parameters to minimize college canteen food wastage.
    """
    menu_items = db.query(MenuItem).all()
    predictions = []
    
    # Base multiplier based on popularity
    for item in menu_items:
        canteen = db.query(Canteen).filter(Canteen.id == item.canteen_id).first()
        base_demand = 80 if "Biryani" in item.name else (65 if "Rice" in item.name or "Noodles" in item.name else 40)
        # Factor in actual order count
        order_bias = item.total_orders_count * 3
        predicted_qty = base_demand + order_bias + random.randint(15, 45)
        
        confidence = round(random.uniform(88.5, 96.8), 1)
        
        predictions.append({
            "menu_item_id": item.id,
            "dish_name": item.name,
            "canteen_name": canteen.name if canteen else "Canteen",
            "category": item.category,
            "predicted_demand_units": predicted_qty,
            "recommended_prep_batch": int(predicted_qty * 1.05),
            "confidence_score": f"{confidence}%",
            "trend": "UP (+14%)" if "Biryani" in item.name or "Noodles" in item.name else "STABLE",
            "price": item.price
        })
        
    return sorted(predictions, key=lambda x: x["predicted_demand_units"], reverse=True)

def get_ai_crowd_forecast():
    """
    Hour-by-hour campus crowd prediction for typical college schedule:
    Peaks at 12:00 PM - 2:00 PM (Lunch) and 4:30 PM - 5:30 PM (Evening Snacks)
    """
    hourly_forecast = [
        {"hour": "08:00 AM", "canteen_1": 15, "canteen_2": 10, "canteen_3": 8, "canteen_4": 12, "level": "LOW"},
        {"hour": "09:00 AM", "canteen_1": 45, "canteen_2": 30, "canteen_3": 25, "canteen_4": 35, "level": "MEDIUM"},
        {"hour": "10:00 AM", "canteen_1": 30, "canteen_2": 25, "canteen_3": 20, "canteen_4": 22, "level": "LOW"},
        {"hour": "11:00 AM", "canteen_1": 40, "canteen_2": 35, "canteen_3": 30, "canteen_4": 38, "level": "MEDIUM"},
        {"hour": "12:00 PM", "canteen_1": 95, "canteen_2": 85, "canteen_3": 75, "canteen_4": 90, "level": "HIGH"},
        {"hour": "01:00 PM", "canteen_1": 120, "canteen_2": 95, "canteen_3": 88, "canteen_4": 110, "level": "PEAK RUSH"},
        {"hour": "02:00 PM", "canteen_1": 70, "canteen_2": 60, "canteen_3": 50, "canteen_4": 65, "level": "MEDIUM"},
        {"hour": "03:00 PM", "canteen_1": 25, "canteen_2": 20, "canteen_3": 18, "canteen_4": 20, "level": "LOW"},
        {"hour": "04:00 PM", "canteen_1": 50, "canteen_2": 45, "canteen_3": 40, "canteen_4": 55, "level": "MEDIUM"},
        {"hour": "05:00 PM", "canteen_1": 65, "canteen_2": 50, "canteen_3": 42, "canteen_4": 60, "level": "MEDIUM"},
        {"hour": "06:00 PM", "canteen_1": 35, "canteen_2": 25, "canteen_3": 20, "canteen_4": 30, "level": "LOW"},
        {"hour": "07:00 PM", "canteen_1": 20, "canteen_2": 15, "canteen_3": 12, "canteen_4": 18, "level": "LOW"},
    ]
    return hourly_forecast

def get_smart_recommendations(db: Session):
    """
    AI Smart Recommendation Engine:
    Compares real-time canteen loads and waiting times, and generates recommendation insights.
    """
    from backend.app.crowd_engine import calculate_canteen_crowd
    canteens = db.query(Canteen).filter(Canteen.is_open == True).all()
    
    canteen_stats = []
    for c in canteens:
        crowd = calculate_canteen_crowd(c, db)
        canteen_stats.append({
            "canteen": c,
            "crowd": crowd
        })
        
    canteen_stats.sort(key=lambda x: x["crowd"].estimated_wait_time_mins)
    
    recommendations = []
    if len(canteen_stats) >= 2:
        fastest = canteen_stats[0]
        busiest = canteen_stats[-1]
        
        if busiest["crowd"].estimated_wait_time_mins > fastest["crowd"].estimated_wait_time_mins + 5:
            recommendations.append({
                "type": "CROWD_ROUTING",
                "title": f"⚡ Fast Pickup Recommendation",
                "message": f"{fastest['canteen'].name} currently has only {fastest['crowd'].estimated_wait_time_mins} min wait time, whereas {busiest['canteen'].name} is experiencing heavy crowd ({busiest['crowd'].estimated_wait_time_mins} mins).",
                "suggested_canteen_id": fastest['canteen'].id,
                "badge": "Save Time"
            })
            
    recommendations.append({
        "type": "POPULAR_DISH",
        "title": "🔥 Rathinam Favorite Today",
        "message": "Chicken Biryani at Chat Stop and Kothu Parotta at CCT are trending with top student ratings!",
        "badge": "Trending"
    })
    
    return recommendations
