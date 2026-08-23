from sqlalchemy.orm import Session
from backend.app.models import User, Canteen, MenuItem, Order, OrderItem, Announcement, Base, engine
from backend.app.auth import hash_password
from datetime import datetime, timedelta

def seed_database(db: Session):
    # Create all tables if not exist
    Base.metadata.create_all(bind=engine)
    
    # Check if already seeded
    if db.query(Canteen).first():
        print("Database already contains data, skipping initial seeding.")
        return

    print("Seeding Rathinam College Canteens and initial demo data...")

    # 1. CREATE CANTEENS
    canteen1 = Canteen(
        name="Chat Stop",
        slug="chat-stop",
        token_prefix="CS",
        description="Famous for hot spicy biryanis, crispy noodles, and flavorful quick bites.",
        location="Near LTM & Rathinam Auditorium",
        image_url="/static/images/canteen_chatstop.jpg",
        is_open=True,
        active_counters=3,
        avg_prep_time_mins=7,
        parcel_fee=10.0,
        parcel_only=False,
        opening_time="08:00 AM",
        closing_time="08:30 PM",
        contact_number="+91 98421 00101"
    )
    
    canteen2 = Canteen(
        name="Z-Cafe",
        slug="z-cafe",
        token_prefix="ZC",
        description="Trendy modern student cafe with delicious fried rice, noodles, and chilled drinks.",
        location="Near LTM & Rathinam Auditorium",
        image_url="/static/images/canteen_zcafe.jpg",
        is_open=True,
        active_counters=2,
        avg_prep_time_mins=5,
        parcel_fee=10.0,
        parcel_only=False,
        opening_time="08:30 AM",
        closing_time="09:00 PM",
        contact_number="+91 98421 00102"
    )
    
    canteen3 = Canteen(
        name="Seyon",
        slug="seyon",
        token_prefix="SY",
        description="Authentic home-style South Indian veg meals, variety rice, and hot freshly prepared lunch plates.",
        location="Opposite to Food Court & Nearby Arts Block",
        image_url="/static/images/canteen_seyon.jpg",
        is_open=True,
        active_counters=2,
        avg_prep_time_mins=4,
        parcel_fee=5.0,
        parcel_only=False,
        opening_time="08:00 AM",
        closing_time="07:30 PM",
        contact_number="+91 98421 00103"
    )
    
    canteen4 = Canteen(
        name="CCT",
        slug="cct",
        token_prefix="CCT",
        description="Central Campus Treat! Famous for aromatic Chicken Biryani, sizzling Kothu Parotta, and comforting meals.",
        location="Opposite Tower A",
        image_url="/static/images/canteen_cct.jpg",
        is_open=True,
        active_counters=3,
        avg_prep_time_mins=6,
        parcel_fee=5.0,
        parcel_only=False,
        opening_time="08:00 AM",
        closing_time="09:30 PM",
        contact_number="+91 98421 00104"
    )
    
    canteen5 = Canteen(
        name="Z-Cafe Juice",
        slug="z-cafe-juice",
        token_prefix="ZJ",
        description="Chilled pure fresh fruit juices, energizing fruit coolers, and refreshing shakes.",
        location="Near LTM & Rathinam Auditorium",
        image_url="/static/images/canteen_juice.jpg",
        is_open=True,
        active_counters=2,
        avg_prep_time_mins=3,
        parcel_fee=5.0,
        parcel_only=False,
        opening_time="08:00 AM",
        closing_time="08:30 PM",
        contact_number="+91 98421 00105"
    )

    db.add_all([canteen1, canteen2, canteen3, canteen4, canteen5])
    db.commit()

    # 2. CREATE USERS
    # Student Accounts
    student1 = User(
        username="darshan",
        email="darshan@rathinam.ac.in",
        password_hash=hash_password("password123"),
        full_name="Darshan R",
        role="STUDENT",
        phone="+91 97890 12345",
        department="CSE-A",
        roll_number="23BCSE101"
    )
    student2 = User(
        username="priya_k",
        email="priya.k@rathinam.ac.in",
        password_hash=hash_password("password123"),
        full_name="Priya K",
        role="STUDENT",
        phone="+91 97890 54321",
        department="ECE-B",
        roll_number="23BECE042"
    )

    # Canteen Owners
    owner1 = User(
        username="chatstop_owner",
        email="chatstop@rathinam.ac.in",
        password_hash=hash_password("password123"),
        full_name="Chat Stop Manager",
        role="CANTEEN_OWNER",
        phone="+91 98421 00101",
        canteen_id=canteen1.id
    )
    owner2 = User(
        username="zcafe_owner",
        email="zcafe@rathinam.ac.in",
        password_hash=hash_password("password123"),
        full_name="Z-Cafe Manager",
        role="CANTEEN_OWNER",
        phone="+91 98421 00102",
        canteen_id=canteen2.id
    )
    owner3 = User(
        username="seyon_owner",
        email="seyon@rathinam.ac.in",
        password_hash=hash_password("password123"),
        full_name="Seyon Food Desk",
        role="CANTEEN_OWNER",
        phone="+91 98421 00103",
        canteen_id=canteen3.id
    )
    owner4 = User(
        username="cct_owner",
        email="cct@rathinam.ac.in",
        password_hash=hash_password("password123"),
        full_name="CCT Cafeteria Incharge",
        role="CANTEEN_OWNER",
        phone="+91 98421 00104",
        canteen_id=canteen4.id
    )
    owner5 = User(
        username="zedcoffee_owner",
        email="zedcoffee@rathinam.ac.in",
        password_hash=hash_password("password123"),
        full_name="Zed Coffee Juice Staff",
        role="CANTEEN_OWNER",
        phone="+91 98421 00105",
        canteen_id=canteen5.id
    )

    # Class Representatives
    cr_ece = User(
        username="cr_ece",
        email="cr.ece@rathinam.ac.in",
        password_hash=hash_password("password123"),
        full_name="Arjun M (ECE-A CR)",
        role="CLASS_REP",
        phone="+91 98940 11223",
        department="ECE-A"
    )
    cr_cse = User(
        username="cr_cse",
        email="cr.cse@rathinam.ac.in",
        password_hash=hash_password("password123"),
        full_name="Sneha R (CSE-B CR)",
        role="CLASS_REP",
        phone="+91 98940 33445",
        department="CSE-B"
    )

    # Admin Account
    admin = User(
        username="admin",
        email="admin@rathinam.ac.in",
        password_hash=hash_password("admin123"),
        full_name="Rathinam Campus Admin",
        role="ADMIN",
        phone="+91 94444 88888",
        department="ADMIN_OFFICE"
    )

    db.add_all([student1, student2, owner1, owner2, owner3, owner4, owner5, cr_ece, cr_cse, admin])
    db.commit()

    # 3. CREATE MENU ITEMS (EXACT ITEMS FROM USER PROMPT)
    # Canteen 1: Chat Stop (foods - chicken rice, chicken noodles, chicken biryani, thokku biryani, chili biryani - rs.100, veg biryani -60, curd rice-60, sambar-60, egg rice -80 (parcel extra rs 10))
    chat_stop_items = [
        MenuItem(canteen_id=canteen1.id, name="Chicken Rice", category="Fried Rice", description="Wok-tossed aromatic rice with tender chicken chunks, spring onions, and special spices.", price=100.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/chicken_rice.jpg", prep_time_mins=8, parcel_price=10.0, total_orders_count=45),
        MenuItem(canteen_id=canteen1.id, name="Chicken Noodles", category="Noodles", description="Hakka style stir-fried noodles with seasoned chicken, crunchy vegetables, and soy glaze.", price=100.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/chicken_noodles.jpg", prep_time_mins=8, parcel_price=10.0, total_orders_count=52),
        MenuItem(canteen_id=canteen1.id, name="Chicken Biryani", category="Biryani", description="Signature slow-cooked Seeraga Samba chicken biryani served with spicy gravy & raita.", price=100.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/chicken_biryani.jpg", prep_time_mins=4, parcel_price=10.0, total_orders_count=88),
        MenuItem(canteen_id=canteen1.id, name="Thokku Biryani", category="Biryani", description="Spicy Chettinad chicken thokku layered over fragrant biryani rice for intense flavor.", price=100.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/thokku_biryani.jpg", prep_time_mins=5, parcel_price=10.0, total_orders_count=60),
        MenuItem(canteen_id=canteen1.id, name="Chili Biryani", category="Biryani", description="Fiery chili-marinated chicken bites tossed with spicy infused biryani rice.", price=100.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/chili_biryani.jpg", prep_time_mins=6, parcel_price=10.0, total_orders_count=35),
        MenuItem(canteen_id=canteen1.id, name="Veg Biryani", category="Biryani", description="Flavorful garden fresh vegetables cooked with fragrant basmati and whole spices.", price=60.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/veg_biryani.jpg", prep_time_mins=4, parcel_price=10.0, total_orders_count=30),
        MenuItem(canteen_id=canteen1.id, name="Curd Rice", category="Rice", description="Soothing tempered creamy curd rice with mustard, ginger, curry leaves, and pickle.", price=60.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/curd_rice.jpg", prep_time_mins=2, parcel_price=10.0, total_orders_count=22),
        MenuItem(canteen_id=canteen1.id, name="Sambar Rice", category="Rice", description="Traditional South Indian piping hot sambar sadham topped with pure ghee & appalam.", price=60.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/sambar_rice.jpg", prep_time_mins=3, parcel_price=10.0, total_orders_count=25),
        MenuItem(canteen_id=canteen1.id, name="Egg Rice", category="Fried Rice", description="Golden wok-tossed fried rice with double scrambled egg, pepper, and spring onion.", price=80.0, is_veg=False, is_egg=True, is_available=True, image_url="/static/images/foods/egg_rice.jpg", prep_time_mins=6, parcel_price=10.0, total_orders_count=48),
    ]

    # Canteen 2: Z-Cafe (foods - chicken rice, chicken noodles, chicken biryani, chili biryani - rs.100, egg rice -80 (parcel extra rs 10))
    zcafe_items = [
        MenuItem(canteen_id=canteen2.id, name="Chicken Rice", category="Fried Rice", description="Z-Cafe special smoky chicken fried rice prepared with fresh capsicum and chili sauce.", price=100.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/chicken_rice.jpg", prep_time_mins=6, parcel_price=10.0, total_orders_count=34),
        MenuItem(canteen_id=canteen2.id, name="Chicken Noodles", category="Noodles", description="Classic street-style chicken noodles tossed in hot wok with chef's secret spice mix.", price=100.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/chicken_noodles.jpg", prep_time_mins=7, parcel_price=10.0, total_orders_count=41),
        MenuItem(canteen_id=canteen2.id, name="Chicken Biryani", category="Biryani", description="Rich Dum biryani cooked with succulent chicken and aromatic saffron-infused rice.", price=100.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/chicken_biryani.jpg", prep_time_mins=4, parcel_price=10.0, total_orders_count=65),
        MenuItem(canteen_id=canteen2.id, name="Chili Biryani", category="Biryani", description="Zesty spicy fried chili chicken pieces combined with spiced dum rice.", price=100.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/chili_biryani.jpg", prep_time_mins=5, parcel_price=10.0, total_orders_count=28),
        MenuItem(canteen_id=canteen2.id, name="Egg Rice", category="Fried Rice", description="Crispy egg scrambled with aromatic basmati rice, green chilies, and coriander.", price=80.0, is_veg=False, is_egg=True, is_available=True, image_url="/static/images/foods/egg_rice.jpg", prep_time_mins=5, parcel_price=10.0, total_orders_count=36),
    ]

    # Canteen 3: Seyon (foods -veg biryani, egg rice, tomato rice, egg noodles - rs 65, curd rice, sambar - rs 55 all incl parcel - rs 5 only parcel aval)
    seyon_items = [
        MenuItem(canteen_id=canteen3.id, name="Veg Biryani", category="Biryani", description="Traditional Seyon special aromatic veg biryani packed fresh with spiced brinjal gravy.", price=65.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/veg_biryani.jpg", prep_time_mins=3, parcel_price=5.0, total_orders_count=40),
        MenuItem(canteen_id=canteen3.id, name="Egg Rice", category="Rice", description="Hot fresh rice tossed with eggs, mustard seeds, and freshly crushed black pepper.", price=65.0, is_veg=False, is_egg=True, is_available=True, image_url="/static/images/foods/egg_rice.jpg", prep_time_mins=4, parcel_price=5.0, total_orders_count=45),
        MenuItem(canteen_id=canteen3.id, name="Tomato Rice", category="Rice", description="Tangy and flavorful country tomato rice tempered with cashews, curry leaves & ghee.", price=65.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/tomato_rice.jpg", prep_time_mins=3, parcel_price=5.0, total_orders_count=32),
        MenuItem(canteen_id=canteen3.id, name="Egg Noodles", category="Noodles", description="Fast express egg noodles loaded with fresh cabbage, carrots, and scrambled egg.", price=65.0, is_veg=False, is_egg=True, is_available=True, image_url="/static/images/foods/egg_noodles.jpg", prep_time_mins=5, parcel_price=5.0, total_orders_count=50),
        MenuItem(canteen_id=canteen3.id, name="Curd Rice", category="Rice", description="Homestyle chilled curd rice with pomegranate seeds and spicy mango pickle.", price=55.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/curd_rice.jpg", prep_time_mins=2, parcel_price=5.0, total_orders_count=38),
        MenuItem(canteen_id=canteen3.id, name="Sambar Rice", category="Rice", description="Hot piping drumstick sambar rice packed in hygienic eco-leaf containers.", price=55.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/sambar_rice.jpg", prep_time_mins=2, parcel_price=5.0, total_orders_count=42),
    ]

    # Canteen 4: CCT (foods - chicken biryani rs-110, egg rice rs-80, kothu parotta rs-80, curd rice -50, sambar -50 parcel rs 5)
    cct_items = [
        MenuItem(canteen_id=canteen4.id, name="Chicken Biryani", category="Biryani", description="CCT King Biryani! Premium chicken pieces, boiled egg, aromatic jeera samba rice & salna.", price=110.0, is_veg=False, is_egg=False, is_available=True, image_url="/static/images/foods/chicken_biryani.jpg", prep_time_mins=4, parcel_price=5.0, total_orders_count=95),
        MenuItem(canteen_id=canteen4.id, name="Egg Rice", category="Fried Rice", description="Wholesome egg fried rice stir-fried on high heat with fresh vegetables and pepper.", price=80.0, is_veg=False, is_egg=True, is_available=True, image_url="/static/images/foods/egg_rice.jpg", prep_time_mins=6, parcel_price=5.0, total_orders_count=55),
        MenuItem(canteen_id=canteen4.id, name="Kothu Parotta", category="Fast Food", description="Crispy shredded Malabar parottas beaten on hot tava with eggs, onions, and rich spicy salna.", price=80.0, is_veg=False, is_egg=True, is_available=True, image_url="/static/images/foods/kothu_parotta.jpg", prep_time_mins=7, parcel_price=5.0, total_orders_count=78),
        MenuItem(canteen_id=canteen4.id, name="Curd Rice", category="Rice", description="Smooth wholesome curd rice with fried mor milagai (chili) and pickle.", price=50.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/curd_rice.jpg", prep_time_mins=2, parcel_price=5.0, total_orders_count=29),
        MenuItem(canteen_id=canteen4.id, name="Sambar Rice", category="Rice", description="Authentic Tamil Nadu sambar sadham with potato fry and crispy appalam.", price=50.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/sambar_rice.jpg", prep_time_mins=2, parcel_price=5.0, total_orders_count=31),
    ]

    # Canteen 5: Zed Coffee Juice (exact requested juices and prices)
    juice_items = [
        MenuItem(canteen_id=canteen5.id, name="Orange Juice", category="Beverages", description="100% Pure fresh Nagpur Valencia orange juice freshly pressed.", price=60.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/orange_juice.jpg", prep_time_mins=3, parcel_price=5.0, total_orders_count=65),
        MenuItem(canteen_id=canteen5.id, name="Watermelon Juice", category="Beverages", description="Hydrating chilled fresh watermelon cooler with chia seeds & crushed ice.", price=30.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/watermelon_juice.jpg", prep_time_mins=2, parcel_price=5.0, total_orders_count=78),
        MenuItem(canteen_id=canteen5.id, name="Muskmelon Juice", category="Beverages", description="Sweet refreshing chilled cantaloupe muskmelon juice prepared fresh.", price=60.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/muskmelon_juice_new.png", prep_time_mins=3, parcel_price=5.0, total_orders_count=42),
        MenuItem(canteen_id=canteen5.id, name="Lime Fresh Juice", category="Beverages", description="Refreshing freshly squeezed lime cooler with mint (Sweet / Salt / Soda).", price=30.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/lime_juice.jpg", prep_time_mins=2, parcel_price=5.0, total_orders_count=85),
        MenuItem(canteen_id=canteen5.id, name="Mango Juice", category="Beverages", description="Rich creamy sweet Alphonso mango pulp juice blended with chilled ice.", price=60.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/mango_juice.jpg", prep_time_mins=3, parcel_price=5.0, total_orders_count=58),
        MenuItem(canteen_id=canteen5.id, name="Papaya Juice", category="Beverages", description="Smooth wholesome tropical ripe papaya juice rich in vitamins.", price=60.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/papaya_juice.jpg", prep_time_mins=3, parcel_price=5.0, total_orders_count=35),
        MenuItem(canteen_id=canteen5.id, name="Pomegranate Juice", category="Beverages", description="Antioxidant-rich fresh ruby red pomegranate pearls cold-pressed pure.", price=120.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/pomegranate_juice_new.png", prep_time_mins=4, parcel_price=5.0, total_orders_count=50),
        MenuItem(canteen_id=canteen5.id, name="Apple Juice", category="Beverages", description="Crisp natural Shimla royal apple juice with no added preservatives.", price=100.0, is_veg=True, is_egg=False, is_available=True, image_url="/static/images/foods/apple_juice.jpg", prep_time_mins=3, parcel_price=5.0, total_orders_count=45),
    ]

    all_items = chat_stop_items + zcafe_items + seyon_items + cct_items + juice_items
    db.add_all(all_items)
    db.commit()

    # 4. CREATE ACTIVE SAMPLE ORDERS (TO SHOWCASE CROWD VARIATION AND TOKENS)
    # Chat Stop has high crowd (e.g. 5 active orders)
    ord1 = Order(
        order_number="RAT-2026-000101",
        token_number="CS-101",
        student_id=student1.id,
        canteen_id=canteen1.id,
        status="PREPARING",
        payment_method="UPI",
        payment_status="PAID",
        upi_transaction_id="UPI-RAT-89201",
        subtotal=200.0,
        parcel_charge=10.0,
        is_parcel=True,
        total_amount=210.0,
        notes="Less spicy please",
        queue_position=2,
        estimated_wait_time_mins=12,
        created_at=datetime.utcnow() - timedelta(minutes=6)
    )
    db.add(ord1)
    db.commit()
    
    db.add(OrderItem(order_id=ord1.id, menu_item_id=chat_stop_items[0].id, item_name="Chicken Rice", quantity=1, unit_price=100.0, subtotal=100.0))
    db.add(OrderItem(order_id=ord1.id, menu_item_id=chat_stop_items[1].id, item_name="Chicken Noodles", quantity=1, unit_price=100.0, subtotal=100.0))

    ord2 = Order(
        order_number="RAT-2026-000102",
        token_number="CS-102",
        student_id=student2.id,
        canteen_id=canteen1.id,
        status="READY_FOR_PICKUP",
        payment_method="UPI",
        payment_status="PAID",
        upi_transaction_id="UPI-RAT-89202",
        subtotal=100.0,
        parcel_charge=0.0,
        is_parcel=False,
        total_amount=100.0,
        queue_position=1,
        estimated_wait_time_mins=0,
        created_at=datetime.utcnow() - timedelta(minutes=15),
        ready_at=datetime.utcnow() - timedelta(minutes=2)
    )
    db.add(ord2)
    db.commit()
    db.add(OrderItem(order_id=ord2.id, menu_item_id=chat_stop_items[2].id, item_name="Chicken Biryani", quantity=1, unit_price=100.0, subtotal=100.0))

    # CCT has active orders
    ord3 = Order(
        order_number="RAT-2026-000103",
        token_number="CCT-101",
        student_id=student1.id,
        canteen_id=canteen4.id,
        status="ORDER_PLACED",
        payment_method="CASH",
        payment_status="PAY_AT_COUNTER",
        subtotal=160.0,
        parcel_charge=5.0,
        is_parcel=True,
        total_amount=165.0,
        queue_position=1,
        estimated_wait_time_mins=6,
        created_at=datetime.utcnow() - timedelta(minutes=2)
    )
    db.add(ord3)
    db.commit()
    db.add(OrderItem(order_id=ord3.id, menu_item_id=cct_items[1].id, item_name="Egg Rice", quantity=2, unit_price=80.0, subtotal=160.0))

    # 5. CREATE INITIAL ANNOUNCEMENTS (CR & CANTEEN UPDATES)
    ann1 = Announcement(
        author_id=cr_ece.id,
        author_role="CLASS_REP",
        author_name="Arjun M (ECE-A CR)",
        title="📢 ECE-A Lunch Break & Canteen Crowd Advisory",
        content="ECE-A lab finishes at 12:35 PM today. Heavy crowd expected at Chat Stop. Students are advised to order at Z-Cafe or Seyon for fast 5-min pickup!",
        target_class="ECE-A",
        broadcast_type="CR_BROADCAST",
        is_active=True
    )
    
    ann2 = Announcement(
        author_id=owner1.id,
        author_role="CANTEEN_OWNER",
        author_name="Chat Stop Manager",
        canteen_id=canteen1.id,
        title="⚡ Extra Express Counter Opened",
        content="We have opened Counter #3 specifically for Biryani & Fried Rice token pickups to reduce waiting time!",
        target_class="ALL",
        broadcast_type="CANTEEN_UPDATE",
        is_active=True
    )

    ann3 = Announcement(
        author_id=admin.id,
        author_role="ADMIN",
        author_name="Rathinam Campus Admin",
        title="🎓 Welcome to Rathinam Smart Canteen Hub",
        content="Students can now track live crowd levels, pay via UPI or Cash, and collect food using digital tokens across Chat Stop, Z-Cafe, Seyon, CCT, and Juice Hub.",
        target_class="ALL",
        broadcast_type="CAMPUS",
        is_active=True
    )

    db.add_all([ann1, ann2, ann3])
    db.commit()
    print("Seeding completed successfully!")
