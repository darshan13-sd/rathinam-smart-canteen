# 🎓 Rathinam College Smart Canteen Hub
### Multi-Canteen Smart Ordering & Campus Crowd Management System

A production-ready full-stack web and mobile-friendly application engineered for **Rathinam College** to eliminate physical canteen queues, provide real-time campus crowd intelligence, support Class Representative broadcasts, and offer seamless digital token tracking with instant WebSocket push updates.

---

## 🌟 Key Highlights & Features

### 1. 🏢 Multi-Canteen Architecture & Locations
Pre-configured with Rathinam College food outlets and exact custom menus:
* **Canteen 1: Chat Stop** (*Near LTM & Rathinam Auditorium*) — Chicken Rice (₹100), Chicken Noodles (₹100), Chicken Biryani (₹100), Thokku Biryani (₹100), Chili Biryani (₹100), Veg Biryani (₹60), Curd Rice (₹60), Sambar Rice (₹60), Egg Rice (₹80) + ₹10/item Parcel option.
* **Canteen 2: Z-Cafe** (*Near LTM & Rathinam Auditorium*) — Chicken Rice (₹100), Chicken Noodles (₹100), Chicken Biryani (₹100), Chili Biryani (₹100), Egg Rice (₹80) + ₹10/item Parcel option.
* **Canteen 3: Seyon** (*Opposite to Food Court & Nearby Arts Block*) — Veg Biryani (₹65), Egg Rice (₹65), Tomato Rice (₹65), Egg Noodles (₹65), Curd Rice (₹55), Sambar Rice (₹55) + ₹5/item Parcel option.
* **Canteen 4: CCT (Central Campus Treat)** (*Opposite Tower A*) — Chicken Biryani (₹110), Egg Rice (₹80), Kothu Parotta (₹80), Curd Rice (₹50), Sambar Rice (₹50) + ₹5/item Parcel option.
* **Canteen 5: Z-Cafe Juice** (*Near LTM & Rathinam Auditorium*) — Chilled Orange Juice (₹60), Watermelon Juice (₹30), Muskmelon Juice (₹60), Lime Fresh Juice (₹30), Mango Juice (₹60), Papaya Juice (₹60), Pomegranate Juice (₹120), Apple Juice (₹100) + ₹5/item Parcel.

---

## 👥 4 Role-Based Workflows

### 👨‍🎓 1. Student Experience
* **Live Campus Crowd Radar**: Compare wait times and crowd levels (🟢 LOW / 🟡 MEDIUM / 🔴 HIGH) across all 5 canteens before placing an order.
* **Per-Item Split Parcel & Dine-In**: Order multiple quantities of the same dish and choose exactly how many to pack as parcel and how many to serve dine-in (e.g. 2 Sambar Rice ➔ 1 Parcel + 1 Dine-in).
* **Closed Canteen Protection**: When a canteen is closed, ordering is automatically blocked with clear warning banners.
* **Order History Filters & Search**: Filter past orders by status (All, Active/Preparing, Ready for Pickup, Completed, Parcel) or search by Token/Dish.
* **Interactive Payments**:
  * **UPI Gateway**: Mock UPI dynamic QR code generator + App buttons (GPay, PhonePe, Paytm, BHIM) + simulation timer.
  * **Cash Counter**: Direct token generation with clear `"PAY AT COUNTER"` indicator.
* **Digital Token & Live Order Stepper**:
  * Large visual Token ID (e.g. `CS-101`, `ZC-102`) & Order ID (`RAT-2026-000184`).
  * 5-stage animated progress bar: `Order Placed` ➔ `Payment Confirmed` ➔ `Preparing` ➔ `Ready for Pickup` ➔ `Completed`.
  * Live Queue Position (e.g. *"Queue #2 — 1 order ahead of you"*).
  * **Audio Notification**: Sound chime alerts the student the second their order is ready!
* **Itemized Digital Receipt** & 1-click **"Order Again"** reordering.

### 🏪 2. Canteen Owner Portal
* **Isolated Canteen Management**: Chat Stop owner only sees Chat Stop orders; Z-Cafe manages Z-Cafe, etc.
* **Live Kanban Queue**: Real-time incoming order alerts with 1-click status advances (`Pending` ➔ `Preparing` ➔ `Ready for Pickup` ➔ `Completed`).
* **Live Stock Switch**: 1-click **"In Stock" / "Out of Stock"** toggle that immediately broadcasts to all connected students via WebSockets without page reload.
* **Instant Canteen Notices & Open/Closed Status Toggle**: Close/Open canteen anytime with live broadcast.

### 📢 3. Class Representative (CR) Portal
* **WhatsApp Broadcast Generator**: Formats rich, emoji-enabled class announcements with real-time canteen crowd advisories.
* **1-Click WhatsApp Share Links**: Direct `https://api.whatsapp.com/send?text=...` links for instant sharing to class groups.
* **Live Crowd Radar**: View all canteen queue loads to guide classmates to faster outlets.

### 🛡️ 4. Campus Administrator Dashboard
* **Campus Analytics**: Real-time revenue counter, total campus orders, peak hour rush graph (11:30 AM – 2:30 PM).
* **AI Demand Forecasting**: Machine Learning batch sizing for tomorrow's lunch dishes to eliminate cafeteria food wastage.
* **AI Crowd Forecast**: Hour-by-hour crowd prediction curve.

---

## ⚡ Quick Start & Running Locally

### 1. Prerequisites
* Python 3.10+ installed

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/darshan13-sd/my-website.git
cd my-website

# Install required Python packages
pip install -r requirements.txt
```

### 3. Start the Server
```bash
# Run the FastAPI server on port 8005 (or default 8000)
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8005 --reload
```

### 4. Open Application in Browser
Open your browser and navigate to:
👉 **`http://127.0.0.1:8005/`**

---

## 🔑 Demo Login Accounts

Use the **Role Switcher dropdown** on the top right navigation bar to effortlessly switch between roles (Password required: `password123` / `admin123`):

| Role | Username | Password | Role Description |
| :--- | :--- | :--- | :--- |
| **Student** | `darshan` | `password123` | Darshan R (CSE-A) — Full ordering flow |
| **Student** | `priya_k` | `password123` | Priya K (ECE-B) — Active order demo |
| **Canteen Owner 1** | `chatstop_owner` | `password123` | Chat Stop Kitchen & Menu Manager |
| **Canteen Owner 2** | `zcafe_owner` | `password123` | Z-Cafe Kitchen Manager |
| **Canteen Owner 3** | `seyon_owner` | `password123` | Seyon Food Desk Manager |
| **Canteen Owner 4** | `cct_owner` | `password123` | CCT Cafeteria Staff |
| **Canteen Owner 5** | `zedcoffee_owner` | `password123` | Z-Cafe Juice Staff |
| **Class Rep (CR)** | `cr_ece` | `password123` | Arjun M (ECE-A CR) — WhatsApp Broadcaster |
| **Class Rep (CR)** | `cr_cse` | `password123` | Sneha R (CSE-B CR) — Class Advisor |
| **Administrator** | `admin` | `admin123` | Campus Administrator — Analytics & AI Forecast |

---

## 🚀 How to Deploy on Cloud (Render / Railway) for Free

1. Push your repository to **GitHub**.
2. Go to **[Render.com](https://render.com/)** or **[Railway.app](https://railway.app/)**.
3. Click **"New Web Service"** and select your GitHub repository.
4. Set:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. Click **Deploy**! Your app will be live on a public URL (e.g. `https://rathinam-canteen.onrender.com`) for all your friends to use on their mobile and laptops!

$$\text{Estimated Wait Time} = \frac{\text{Active Orders (Pending + Preparing)} \times \text{Average Prep Time}}{\text{Active Counters}} + \text{Queue Buffer}$$

* 🟢 **LOW**: $< 10$ minutes wait time
* 🟡 **MEDIUM**: $10 - 20$ minutes wait time
* 🔴 **HIGH**: $> 20$ minutes wait time

---

## 🛠️ Technology Stack

* **Backend**: FastAPI (Python), SQLAlchemy ORM, WebSockets
* **Database**: SQLite / PostgreSQL
* **Frontend**: HTML5, Modern TypeScript/JavaScript, Tailwind CSS, Lucide Icons, Chart.js, QRCode.js
* **Branding**: Official Rathinam College logo & color palette
