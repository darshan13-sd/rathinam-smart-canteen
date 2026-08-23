import urllib.parse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.models import Announcement, Canteen, User, get_db
from backend.app.schemas import AnnouncementCreate, AnnouncementResponse
from backend.app.auth import require_auth
from backend.app.websocket_manager import ws_manager
from backend.app.crowd_engine import calculate_canteen_crowd

router = APIRouter(prefix="/api/announcements", tags=["Announcements"])

def serialize_announcement(a: Announcement, db: Session) -> dict:
    canteen = db.query(Canteen).filter(Canteen.id == a.canteen_id).first() if a.canteen_id else None
    
    # Generate WhatsApp formatted share message
    encoded_text = urllib.parse.quote(
        f"🍱 *Rathinam Campus Canteen Update*\n\n"
        f"📌 *{a.title}*\n"
        f"{a.content}\n\n"
        f"— Posted by {a.author_name} ({a.author_role})\n"
        f"⚡ Order online & skip queue on Rathinam Smart Canteen Hub"
    )
    whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_text}"
    
    return {
        "id": a.id,
        "author_id": a.author_id,
        "author_role": a.author_role,
        "author_name": a.author_name,
        "title": a.title,
        "content": a.content,
        "canteen_id": a.canteen_id,
        "canteen_name": canteen.name if canteen else None,
        "target_class": a.target_class,
        "broadcast_type": a.broadcast_type,
        "is_active": a.is_active,
        "created_at": a.created_at,
        "whatsapp_share_url": whatsapp_url
    }

@router.get("", response_model=List[AnnouncementResponse])
def get_announcements(
    target_class: Optional[str] = None,
    canteen_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Announcement).filter(Announcement.is_active == True)
    if canteen_id:
        query = query.filter((Announcement.canteen_id == canteen_id) | (Announcement.canteen_id == None))
    if target_class and target_class != "ALL":
        query = query.filter((Announcement.target_class == target_class) | (Announcement.target_class == "ALL") | (Announcement.target_class == None))
    
    announcements = query.order_by(Announcement.created_at.desc()).all()
    return [serialize_announcement(a, db) for a in announcements]

@router.post("", response_model=AnnouncementResponse)
async def create_announcement(
    payload: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    ann = Announcement(
        author_id=current_user.id,
        author_role=current_user.role,
        author_name=current_user.full_name,
        title=payload.title,
        content=payload.content,
        canteen_id=payload.canteen_id or (current_user.canteen_id if current_user.role == "CANTEEN_OWNER" else None),
        target_class=payload.target_class or "ALL",
        broadcast_type=payload.broadcast_type,
        is_active=True
    )
    db.add(ann)
    db.commit()
    db.refresh(ann)
    
    serialized = serialize_announcement(ann, db)
    await ws_manager.broadcast_event("new_announcement", serialized)
    return serialized

@router.get("/generate-cr-broadcast")
def generate_cr_broadcast(target_class: str = "ECE-A", leave_time: str = "12:30 PM", db: Session = Depends(get_db)):
    """
    Auto-generates a smart WhatsApp broadcast message with live crowd summary for CRs.
    """
    canteens = db.query(Canteen).filter(Canteen.is_open == True).all()
    crowd_lines = []
    recommended_canteen = None
    min_wait = 999
    
    for c in canteens:
        info = calculate_canteen_crowd(c, db)
        emoji = "🟢" if info.crowd_level == "LOW" else ("🟡" if info.crowd_level == "MEDIUM" else "🔴")
        crowd_lines.append(f"• {c.name} — {emoji} {info.crowd_level} (~{info.estimated_wait_time_mins}m wait)")
        if info.estimated_wait_time_mins < min_wait:
            min_wait = info.estimated_wait_time_mins
            recommended_canteen = c.name
            
    crowd_summary = "\n".join(crowd_lines)
    
    message_text = (
        f"🍱 *Campus Canteen Update for {target_class}*\n\n"
        f"Class will leave at *{leave_time}* today.\n\n"
        f"📊 *Current Canteen Crowd Status:*\n"
        f"{crowd_summary}\n\n"
        f"💡 *Advice:* Students are advised to use *{recommended_canteen or 'Z-Cafe'}* to avoid rush.\n"
        f"🚀 Pre-order online to collect via Token: Rathinam Canteen Hub"
    )
    
    encoded = urllib.parse.quote(message_text)
    return {
        "target_class": target_class,
        "leave_time": leave_time,
        "recommended_canteen": recommended_canteen,
        "message_text": message_text,
        "whatsapp_url": f"https://api.whatsapp.com/send?text={encoded}",
        "whatsapp_web_url": f"https://web.whatsapp.com/send?text={encoded}"
    }
