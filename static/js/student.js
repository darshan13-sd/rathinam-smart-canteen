// Student Ordering, Cart, Live Token Tracker & Crowd Radar Logic

let allCanteensData = [];
let selectedCanteen = null;
let currentCanteenMenuItems = [];
let pendingCollisionItem = null;
let activeStudentOrder = null;

// Cart Structure
window.cart = {
  canteenId: null,
  canteenName: '',
  tokenPrefix: '',
  parcelFee: 10.0,
  parcelOnly: false,
  isParcel: false,
  notes: '',
  items: [] // { id, name, price, quantity, image_url, is_veg }
};

async function loadStudentDashboard() {
  await refreshCanteens();
  await loadStudentOrders();
  await loadCampusAnnouncements();
  await loadAIRecommendations();
}

function selectStudentTab(tabName) {
  document.querySelectorAll(".student-tab-btn").forEach(btn => {
    if (btn.dataset.tab === tabName) {
      btn.className = "student-tab-btn active px-4 py-2.5 font-bold text-sm border-b-2 border-rathinam-purple text-rathinam-purple flex items-center gap-2";
    } else {
      btn.className = "student-tab-btn px-4 py-2.5 font-semibold text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-900 flex items-center gap-2";
    }
  });

  document.querySelectorAll(".mobile-nav-item").forEach(btn => {
    if (btn.dataset.tab === tabName) {
      btn.classList.add("text-rathinam-purple");
      btn.classList.remove("text-slate-400");
    } else {
      btn.classList.remove("text-rathinam-purple");
      btn.classList.add("text-slate-400");
    }
  });

  document.querySelectorAll(".student-tab-content").forEach(el => el.classList.add("hidden"));
  const target = document.getElementById(`student-tab-${tabName}`);
  if (target) target.classList.remove("hidden");

  if (tabName === "canteens" && !selectedCanteen) {
    document.getElementById("canteens-list-view").classList.remove("hidden");
    document.getElementById("canteen-menu-header").classList.add("hidden");
  }

  if (window.lucide) lucide.createIcons();
}

async function refreshCanteens() {
  try {
    const res = await fetch("/api/canteens");
    allCanteensData = await res.json();
    renderHomeCanteenGrid(allCanteensData);
    renderAllCanteensFullGrid(allCanteensData);
    updateTopCampusCrowdStatus(allCanteensData);
  } catch (e) {
    console.error("Error loading canteens:", e);
  }
}

function updateTopCampusCrowdStatus(canteens) {
  const statusText = document.getElementById("campus-crowd-status-text");
  if (!statusText || !canteens.length) return;

  const totalActive = canteens.reduce((sum, c) => sum + (c.crowd_info ? c.crowd_info.active_orders : 0), 0);
  const avgWait = Math.round(canteens.reduce((sum, c) => sum + (c.crowd_info ? c.crowd_info.estimated_wait_time_mins : 5), 0) / canteens.length);

  if (avgWait <= 6) {
    statusText.className = "font-bold text-emerald-600";
    statusText.innerText = `LOW RUSH (~${avgWait}m avg wait)`;
  } else if (avgWait <= 15) {
    statusText.className = "font-bold text-amber-600";
    statusText.innerText = `MODERATE (~${avgWait}m avg wait)`;
  } else {
    statusText.className = "font-bold text-rose-600";
    statusText.innerText = `PEAK RUSH (~${avgWait}m avg wait)`;
  }
}

function renderHomeCanteenGrid(canteens) {
  const container = document.getElementById("home-canteens-grid");
  if (!container) return;

  container.innerHTML = canteens.map(c => {
    const crowd = c.crowd_info || { crowd_level: "LOW", estimated_wait_time_mins: 5, active_orders: 0 };
    let crowdBadge = '<span class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 flex items-center gap-1.5 shadow-sm"><span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Low Rush</span>';
    
    if (!c.is_open) {
      crowdBadge = '<span class="px-2.5 py-1 rounded-full text-[11px] font-black bg-rose-100 text-rose-700 border border-rose-200 flex items-center gap-1"><i data-lucide="lock" class="w-3 h-3 text-rose-600"></i> CLOSED</span>';
    } else if (crowd.crowd_level === "MEDIUM") {
      crowdBadge = '<span class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-amber-100 text-amber-800 flex items-center gap-1.5 shadow-sm"><span class="w-2 h-2 rounded-full bg-amber-500"></span> Moderate</span>';
    } else if (crowd.crowd_level === "HIGH") {
      crowdBadge = '<span class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-rose-100 text-rose-800 flex items-center gap-1.5 shadow-sm"><span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span> High Rush</span>';
    }

    return `
      <div class="interactive-card bg-white rounded-2xl border ${!c.is_open ? 'border-rose-200 bg-rose-50/20 opacity-85' : 'border-slate-200/90'} p-4 shadow-sm hover:shadow-md cursor-pointer flex flex-col justify-between" onclick="handleCanteenCardClick(${c.id}, ${c.is_open}, '${c.name.replace(/'/g, "\\'")}')">
        <div>
          <div class="flex items-start justify-between gap-2 mb-2">
            <div>
              <h4 class="font-extrabold text-slate-900 text-base leading-snug">
                ${c.name}
              </h4>
              <span class="inline-flex items-center gap-1 text-[11px] font-bold text-rathinam-purple mt-0.5">
                <i data-lucide="map-pin" class="w-3 h-3 text-rathinam-orange"></i> ${c.location || 'Campus'}
              </span>
            </div>
            ${crowdBadge}
          </div>
          <p class="text-xs text-slate-500 line-clamp-2 mb-3 leading-relaxed">${c.description || ''}</p>
          
          ${c.is_open ? `
            <div class="grid grid-cols-2 gap-2 bg-slate-50 border border-slate-100 p-2.5 rounded-xl text-xs mb-3">
              <div>
                <span class="text-[10px] text-slate-400 block font-bold uppercase tracking-wider">Est. Wait</span>
                <span class="font-black text-amber-600">~ ${crowd.estimated_wait_time_mins} mins</span>
              </div>
              <div>
                <span class="text-[10px] text-slate-400 block font-bold uppercase tracking-wider">Queue</span>
                <span class="font-bold text-slate-800">${crowd.active_orders} active orders</span>
              </div>
            </div>
          ` : `
            <div class="bg-rose-50 border border-rose-200 p-2.5 rounded-xl text-xs mb-3 text-center">
              <span class="text-xs font-bold text-rose-700 flex items-center justify-center gap-1">
                <i data-lucide="lock" class="w-3.5 h-3.5"></i> Currently Closed
              </span>
              <span class="text-[10px] text-rose-500 font-semibold">Not taking orders right now</span>
            </div>
          `}
        </div>

        <div class="flex items-center justify-between pt-2.5 border-t border-slate-100">
          <span class="text-[11px] font-bold text-slate-500 flex items-center gap-1">
            <i data-lucide="package" class="w-3.5 h-3.5 text-slate-400"></i> Parcel: ₹${c.parcel_fee}/item
          </span>
          ${c.is_open ? `
            <button class="px-3.5 py-1.5 rounded-xl bg-slate-900 hover:bg-rathinam-purple text-white text-xs font-extrabold transition flex items-center gap-1 shadow-sm">
              Order <i data-lucide="chevron-right" class="w-3.5 h-3.5"></i>
            </button>
          ` : `
            <span class="px-3 py-1.5 rounded-xl bg-rose-100 text-rose-700 text-xs font-black flex items-center gap-1 cursor-not-allowed">
              <i data-lucide="lock" class="w-3.5 h-3.5"></i> Closed
            </span>
          `}
        </div>
      </div>
    `;
  }).join("");

  if (window.lucide) lucide.createIcons();
}

function handleCanteenCardClick(canteenId, isOpen, canteenName) {
  if (!isOpen) {
    showToast(`${canteenName} is currently CLOSED. It cannot be opened and is not accepting orders!`, "error");
    return;
  }
  openCanteenMenu(canteenId);
}

function renderAllCanteensFullGrid(canteens) {
  const container = document.getElementById("all-canteens-full-grid");
  if (!container) return;

  container.innerHTML = canteens.map(c => {
    const crowd = c.crowd_info || { crowd_level: "LOW", estimated_wait_time_mins: 5, active_orders: 0 };
    return `
      <div class="interactive-card bg-white rounded-2xl border ${!c.is_open ? 'border-rose-200 opacity-85' : 'border-slate-200/90'} overflow-hidden shadow-sm hover:shadow-md transition flex flex-col justify-between">
        <div>
          <div class="h-40 bg-slate-800 relative group overflow-hidden">
            <img src="${c.image_url}" alt="${c.name}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/30 to-transparent flex items-end p-4">
              <div>
                <h3 class="text-lg font-black text-white leading-tight">${c.name}</h3>
                <p class="text-xs text-purple-200 font-semibold flex items-center gap-1 mt-0.5">
                  <i data-lucide="map-pin" class="w-3.5 h-3.5 text-amber-400"></i> ${c.location || 'Rathinam College Campus'}
                </p>
              </div>
            </div>
            ${!c.is_open ? `
              <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-[2px] flex flex-col items-center justify-center text-center p-4">
                <div class="w-10 h-10 rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/40 flex items-center justify-center mb-1">
                  <i data-lucide="lock" class="w-5 h-5"></i>
                </div>
                <span class="text-white font-black text-sm tracking-wide">CANTEEN CLOSED</span>
                <span class="text-rose-300 text-[11px] font-semibold">Not taking orders</span>
              </div>
            ` : `
              <div class="absolute top-3 right-3 bg-white/90 backdrop-blur-md px-2.5 py-1 rounded-full text-[10px] font-black text-emerald-800 border border-white/40 flex items-center gap-1.5 shadow-sm">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> ~${crowd.estimated_wait_time_mins}m wait
              </div>
            `}
          </div>
          <div class="p-4 space-y-3">
            <p class="text-xs text-slate-600 leading-relaxed">${c.description || ''}</p>
            
            ${c.is_open ? `
              <div class="flex items-center justify-between text-xs py-2 px-3 rounded-xl bg-slate-50 border border-slate-100">
                <div><span class="text-slate-400 font-semibold">Queue:</span> <span class="font-extrabold text-slate-800">${crowd.active_orders} orders</span></div>
                <div><span class="text-slate-400 font-semibold">Wait:</span> <span class="font-extrabold text-amber-600">~${crowd.estimated_wait_time_mins}m</span></div>
                <div><span class="text-slate-400 font-semibold">Counters:</span> <span class="font-extrabold text-slate-800">${c.active_counters}</span></div>
              </div>
            ` : `
              <div class="p-2.5 rounded-xl bg-rose-50 border border-rose-200 text-center text-xs font-bold text-rose-700">
                🚫 Canteen is temporarily closed by kitchen
              </div>
            `}
          </div>
        </div>

        <div class="p-4 pt-0">
          <div class="flex items-center justify-between pt-3 border-t border-slate-100">
            <span class="text-xs font-bold text-slate-500">Parcel: +₹${c.parcel_fee}/item</span>
            ${c.is_open ? `
              <button onclick="openCanteenMenu(${c.id})" class="px-4 py-2 rounded-xl bg-rathinam-purple hover:bg-rathinam-purple-dark text-white font-extrabold text-xs transition flex items-center gap-1.5 shadow-sm">
                <i data-lucide="utensils" class="w-4 h-4"></i> View Menu (${(c.menu_items || []).length} items)
              </button>
            ` : `
              <button onclick="showToast('${c.name.replace(/'/g, "\\'")} is currently CLOSED. Menu is unavailable.', 'error')" class="px-4 py-2 rounded-xl bg-rose-100 text-rose-700 font-extrabold text-xs flex items-center gap-1.5 cursor-not-allowed border border-rose-200">
                <i data-lucide="lock" class="w-4 h-4"></i> Canteen Closed
              </button>
            `}
          </div>
        </div>
      </div>
    `;
  }).join("");

  if (window.lucide) lucide.createIcons();
}

async function openCanteenMenu(canteenId) {
  selectedCanteen = allCanteensData.find(c => c.id === canteenId);
  if (!selectedCanteen) return;

  selectStudentTab("canteens");
  document.getElementById("canteens-list-view").classList.add("hidden");
  document.getElementById("canteen-menu-header").classList.remove("hidden");

  // Populate Hero
  const crowd = selectedCanteen.crowd_info || { crowd_level: "LOW", estimated_wait_time_mins: 5, active_orders: 0 };
  const hero = document.getElementById("selected-canteen-hero");
  
  if (!selectedCanteen.is_open) {
    hero.innerHTML = `
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-500/30 text-rose-100 text-xs font-black border border-rose-400/40 mb-2">
            <i data-lucide="lock" class="w-3.5 h-3.5 text-rose-300"></i> CANTEEN IS CURRENTLY CLOSED
          </div>
          <h2 class="text-2xl sm:text-3xl font-black text-white flex items-center gap-3">
            ${selectedCanteen.name}
            <span class="px-2.5 py-0.5 rounded-full bg-rose-600 text-white text-xs font-extrabold">CLOSED</span>
          </h2>
          <p class="text-xs text-rose-200 mt-1 max-w-xl">${selectedCanteen.description || ''}</p>
          <div class="mt-3 p-3 rounded-xl bg-rose-950/60 border border-rose-500/40 text-rose-200 text-xs font-bold flex items-center gap-2">
            <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-400 flex-shrink-0"></i>
            <span>The kitchen is currently closed by the owner and is not accepting orders right now.</span>
          </div>
          <div class="flex flex-wrap items-center gap-3 mt-3 text-xs text-slate-300">
            <span class="flex items-center gap-1"><i data-lucide="map-pin" class="w-3.5 h-3.5 text-amber-400"></i> ${selectedCanteen.location}</span>
            <span class="flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5 text-emerald-400"></i> ${selectedCanteen.opening_time} - ${selectedCanteen.closing_time}</span>
          </div>
        </div>
        <div class="bg-rose-950/50 backdrop-blur-md p-4 rounded-2xl border border-rose-500/30 text-center min-w-[140px]">
          <span class="text-[10px] text-rose-300 uppercase font-bold tracking-wider">Kitchen Status</span>
          <div class="text-2xl font-black text-rose-400 mt-0.5 flex items-center justify-center gap-1"><i data-lucide="lock" class="w-5 h-5"></i> CLOSED</div>
          <span class="text-[10px] text-rose-300 font-bold">Orders Paused</span>
        </div>
      </div>
    `;
  } else {
    hero.innerHTML = `
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 text-white text-xs font-bold mb-2">
            Token Code: ${selectedCanteen.token_prefix}
          </div>
          <h2 class="text-2xl sm:text-3xl font-black text-white">${selectedCanteen.name}</h2>
          <p class="text-xs text-purple-200 mt-1 max-w-xl">${selectedCanteen.description || ''}</p>
          <div class="flex flex-wrap items-center gap-3 mt-3 text-xs text-slate-300">
            <span class="flex items-center gap-1"><i data-lucide="map-pin" class="w-3.5 h-3.5 text-amber-400"></i> ${selectedCanteen.location}</span>
            <span class="flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5 text-emerald-400"></i> ${selectedCanteen.opening_time} - ${selectedCanteen.closing_time}</span>
            <span class="flex items-center gap-1"><i data-lucide="package" class="w-3.5 h-3.5 text-sky-400"></i> Parcel Fee: ₹${selectedCanteen.parcel_fee}</span>
          </div>
        </div>
        <div class="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 text-center min-w-[140px]">
          <span class="text-[10px] text-purple-200 uppercase font-bold tracking-wider">Live Wait Time</span>
          <div class="text-3xl font-black text-amber-300 mt-0.5">~ ${crowd.estimated_wait_time_mins}m</div>
          <span class="text-[10px] text-emerald-300 font-bold">${crowd.active_orders} orders in queue</span>
        </div>
      </div>
    `;
  }

  // Fetch menu
  try {
    const res = await fetch(`/api/menu?canteen_id=${canteenId}`);
    currentCanteenMenuItems = await res.json();
    renderCanteenMenuItems(currentCanteenMenuItems);
  } catch (e) {
    console.error("Error fetching menu items:", e);
  }

  if (window.lucide) lucide.createIcons();
}

function backToCanteensList() {
  selectedCanteen = null;
  document.getElementById("canteen-menu-header").classList.add("hidden");
  document.getElementById("canteens-list-view").classList.remove("hidden");
}

function filterMenuCategory(category) {
  document.querySelectorAll(".menu-filter-btn").forEach(btn => {
    if (btn.dataset.cat === category) {
      btn.className = "menu-filter-btn active px-3.5 py-1.5 rounded-full bg-slate-900 text-white";
    } else {
      btn.className = "menu-filter-btn px-3.5 py-1.5 rounded-full bg-slate-100 text-slate-700 hover:bg-slate-200";
    }
  });

  if (category === "ALL") {
    renderCanteenMenuItems(currentCanteenMenuItems);
  } else if (category === "VEG") {
    renderCanteenMenuItems(currentCanteenMenuItems.filter(i => i.is_veg));
  } else if (category === "NON_VEG") {
    renderCanteenMenuItems(currentCanteenMenuItems.filter(i => !i.is_veg && !i.is_egg));
  } else if (category === "EGG") {
    renderCanteenMenuItems(currentCanteenMenuItems.filter(i => i.is_egg));
  } else if (category === "FAST") {
    renderCanteenMenuItems(currentCanteenMenuItems.filter(i => i.prep_time_mins <= 4));
  }
}

function renderCanteenMenuItems(items) {
  const container = document.getElementById("canteen-menu-grid");
  if (!container) return;

  const isCanteenOpen = selectedCanteen ? selectedCanteen.is_open : true;

  if (!items.length) {
    container.innerHTML = `
      <div class="col-span-full text-center py-10 bg-white rounded-2xl border border-slate-200">
        <i data-lucide="soup" class="w-10 h-10 text-slate-300 mx-auto mb-2"></i>
        <p class="text-sm font-bold text-slate-700">No food items found matching this filter</p>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  container.innerHTML = items.map(item => {
    let dietBadge = '<span class="veg-badge mr-1.5"></span>';
    if (item.is_egg) dietBadge = '<span class="egg-badge mr-1.5"></span>';
    else if (!item.is_veg) dietBadge = '<span class="non-veg-badge mr-1.5"></span>';

    const inCartQty = getCartItemQty(item.id);

    return `
      <div class="interactive-card bg-white rounded-2xl border ${!isCanteenOpen ? 'border-rose-200 opacity-80' : 'border-slate-200/90'} overflow-hidden shadow-sm hover:shadow-md transition flex flex-col justify-between ${!item.is_available ? 'opacity-60' : ''}">
        <div>
          <div class="h-36 bg-slate-100 relative group overflow-hidden">
            <img src="${item.image_url || '/static/images/foods/chicken_biryani.jpg'}" alt="${item.name}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
            <div class="absolute top-2.5 right-2.5 bg-slate-950/80 backdrop-blur-md px-2.5 py-1 rounded-xl text-white font-black text-xs border border-white/20 shadow-sm">
              ₹ ${item.price}
            </div>
            ${!isCanteenOpen ? `
              <div class="absolute inset-0 bg-slate-950/75 backdrop-blur-[2px] flex items-center justify-center text-rose-300 text-xs font-black uppercase tracking-wider gap-1.5">
                <i data-lucide="lock" class="w-4 h-4"></i> Canteen Closed
              </div>
            ` : (!item.is_available ? '<div class="absolute inset-0 bg-slate-900/80 backdrop-blur-[2px] flex items-center justify-center text-white text-xs font-black uppercase tracking-wider">Currently Out of Stock</div>' : '')}
          </div>

          <div class="p-3.5 space-y-1.5">
            <div class="flex items-center justify-between">
              <h4 class="font-extrabold text-slate-900 text-sm flex items-center leading-snug">
                ${dietBadge} ${item.name}
              </h4>
            </div>
            <p class="text-[11px] text-slate-500 line-clamp-2 leading-relaxed">${item.description || ''}</p>
            <div class="flex items-center gap-2 text-[10px] text-slate-400 font-semibold pt-1">
              <span class="text-amber-600 font-bold">⚡ ~${item.prep_time_mins}m prep</span>
              <span>•</span>
              <span class="text-slate-500">🔥 ${item.total_orders_count || 20}+ ordered today</span>
            </div>
          </div>
        </div>

        <div class="p-3.5 pt-0">
          ${!isCanteenOpen ? `
            <button disabled class="w-full py-2.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 font-extrabold text-xs cursor-not-allowed flex items-center justify-center gap-1.5 shadow-sm">
              <i data-lucide="lock" class="w-3.5 h-3.5"></i> Closed (Cannot Order)
            </button>
          ` : (item.is_available ? `
            <div class="flex items-center justify-between gap-2 mt-2 pt-2 border-t border-slate-100">
              <span class="text-sm font-black text-slate-900">₹ ${item.price}</span>
              ${inCartQty > 0 ? `
                <div class="flex items-center gap-2 bg-purple-50 rounded-xl p-1 border border-purple-200">
                  <button onclick="decrementCartItem(${item.id})" class="w-7 h-7 rounded-lg bg-white text-rathinam-purple font-black shadow-sm hover:bg-purple-100 flex items-center justify-center">-</button>
                  <span class="text-xs font-black text-rathinam-purple px-1.5">${inCartQty}</span>
                  <button onclick="incrementCartItem(${item.id})" class="w-7 h-7 rounded-lg bg-rathinam-purple text-white font-black shadow-sm hover:bg-rathinam-purple-dark flex items-center justify-center">+</button>
                </div>
              ` : `
                <button onclick="addItemToCart(${item.id})" class="px-4 py-2 rounded-xl bg-rathinam-purple hover:bg-rathinam-purple-dark text-white font-extrabold text-xs transition shadow-sm flex items-center gap-1.5 active:scale-95">
                  <i data-lucide="plus" class="w-3.5 h-3.5"></i> Add to Cart
                </button>
              `}
            </div>
          ` : `
            <button disabled class="w-full py-2.5 rounded-xl bg-slate-100 text-slate-400 font-extrabold text-xs cursor-not-allowed">
              Out of Stock
            </button>
          `)}
        </div>
      </div>
    `;
  }).join("");

  if (window.lucide) lucide.createIcons();
}

function getCartItemQty(itemId) {
  const found = window.cart.items.find(i => i.id === itemId);
  return found ? found.quantity : 0;
}

function addItemToCart(itemId) {
  if (!selectedCanteen || !selectedCanteen.is_open) {
    showToast(selectedCanteen ? `${selectedCanteen.name} is currently CLOSED. Cannot add items!` : "Canteen is closed", "error");
    return;
  }
  const item = currentCanteenMenuItems.find(i => i.id === itemId);
  if (!item) return;
  if (!item.is_available) {
    showToast(`${item.name} is currently Out of Stock!`, "error");
    return;
  }

  // Single Canteen Check
  if (window.cart.canteenId && window.cart.canteenId !== selectedCanteen.id && window.cart.items.length > 0) {
    pendingCollisionItem = { item, canteen: selectedCanteen };
    document.getElementById("collision-modal-msg").innerHTML = `
      You already have items in your cart from <span class="font-bold text-slate-900">${window.cart.canteenName}</span>.<br/>
      Would you like to start a fresh order for <span class="font-bold text-rathinam-purple">${selectedCanteen.name}</span>?
    `;
    document.getElementById("canteen-collision-modal").classList.remove("hidden");
    return;
  }

  // Set canteen context
  window.cart.canteenId = selectedCanteen.id;
  window.cart.canteenName = selectedCanteen.name;
  window.cart.tokenPrefix = selectedCanteen.token_prefix;
  window.cart.parcelFee = selectedCanteen.parcel_fee || 10.0;
  window.cart.parcelOnly = selectedCanteen.parcel_only || false;
  if (selectedCanteen.parcel_only) window.cart.isParcel = true;

  const existing = window.cart.items.find(i => i.id === item.id);
  if (existing) {
    existing.quantity += 1;
    if (window.cart.parcelOnly || window.cart.isParcel) {
      existing.parcel_quantity = (existing.parcel_quantity || 0) + 1;
    }
  } else {
    window.cart.items.push({
      id: item.id,
      name: item.name,
      price: item.price,
      quantity: 1,
      parcel_quantity: (window.cart.parcelOnly || window.cart.isParcel) ? 1 : 0,
      image_url: item.image_url,
      is_veg: item.is_veg
    });
  }

  updateCartUI();
  renderCanteenMenuItems(currentCanteenMenuItems);
  showToast(`Added "${item.name}" to cart`, "success");
}

function incrementCartItem(itemId) {
  const found = window.cart.items.find(i => i.id === itemId);
  if (found) {
    found.quantity += 1;
    if (window.cart.parcelOnly || window.cart.isParcel) {
      found.parcel_quantity = (found.parcel_quantity || 0) + 1;
    }
    updateCartUI();
    if (selectedCanteen) renderCanteenMenuItems(currentCanteenMenuItems);
  }
}

function decrementCartItem(itemId) {
  const idx = window.cart.items.findIndex(i => i.id === itemId);
  if (idx > -1) {
    if (window.cart.items[idx].quantity > 1) {
      window.cart.items[idx].quantity -= 1;
      window.cart.items[idx].parcel_quantity = Math.min(window.cart.items[idx].parcel_quantity || 0, window.cart.items[idx].quantity);
    } else {
      window.cart.items.splice(idx, 1);
      if (window.cart.items.length === 0) {
        window.cart.canteenId = null;
        window.cart.canteenName = '';
      }
    }
    updateCartUI();
    if (selectedCanteen) renderCanteenMenuItems(currentCanteenMenuItems);
  }
}

function confirmCanteenSwitch() {
  if (!pendingCollisionItem) return;
  window.cart.items = [];
  window.cart.canteenId = pendingCollisionItem.canteen.id;
  window.cart.canteenName = pendingCollisionItem.canteen.name;
  window.cart.tokenPrefix = pendingCollisionItem.canteen.token_prefix;
  window.cart.parcelFee = pendingCollisionItem.canteen.parcel_fee;
  window.cart.parcelOnly = pendingCollisionItem.canteen.parcel_only;
  window.cart.isParcel = pendingCollisionItem.canteen.parcel_only || false;

  window.cart.items.push({
    id: pendingCollisionItem.item.id,
    name: pendingCollisionItem.item.name,
    price: pendingCollisionItem.item.price,
    quantity: 1,
    parcel_quantity: pendingCollisionItem.canteen.parcel_only ? 1 : 0,
    image_url: pendingCollisionItem.item.image_url,
    is_veg: pendingCollisionItem.item.is_veg
  });

  closeCollisionModal();
  updateCartUI();
  renderCanteenMenuItems(currentCanteenMenuItems);
  showToast(`Cart switched to ${window.cart.canteenName}`, "info");
}

function closeCollisionModal() {
  pendingCollisionItem = null;
  document.getElementById("canteen-collision-modal").classList.add("hidden");
}

function setItemParcelStatus(itemId, isParcel) {
  const item = window.cart.items.find(i => i.id === itemId);
  if (item) {
    item.parcel_quantity = isParcel ? item.quantity : 0;
    const allParcel = window.cart.items.length > 0 && window.cart.items.every(i => (i.parcel_quantity || 0) === i.quantity);
    window.cart.isParcel = allParcel;
    const parcelCheckbox = document.getElementById("cart-parcel-checkbox");
    if (parcelCheckbox) parcelCheckbox.checked = allParcel;
    updateCartUI();
  }
}

function changeItemParcelQty(itemId, delta) {
  const item = window.cart.items.find(i => i.id === itemId);
  if (item) {
    if (window.cart.parcelOnly) {
      item.parcel_quantity = item.quantity;
    } else {
      const current = item.parcel_quantity || 0;
      item.parcel_quantity = Math.max(0, Math.min(item.quantity, current + delta));
    }
    const allParcel = window.cart.items.length > 0 && window.cart.items.every(i => (i.parcel_quantity || 0) === i.quantity);
    window.cart.isParcel = allParcel;
    const parcelCheckbox = document.getElementById("cart-parcel-checkbox");
    if (parcelCheckbox) parcelCheckbox.checked = allParcel;
    updateCartUI();
  }
}

function updateCartParcelToggle(isChecked) {
  window.cart.isParcel = isChecked;
  window.cart.items.forEach(it => {
    it.parcel_quantity = isChecked ? it.quantity : 0;
  });
  updateCartUI();
}

function updateCartUI() {
  const totalCount = window.cart.items.reduce((sum, i) => sum + i.quantity, 0);
  const countBadge = document.getElementById("nav-cart-count");
  if (countBadge) countBadge.innerText = totalCount;

  // Cart Drawer Header & Label
  const nameLabel = document.getElementById("cart-canteen-name");
  if (nameLabel) nameLabel.innerText = window.cart.canteenName || "No canteen selected";

  const parcelRatePerItem = window.cart.parcelFee || 10.0;
  const isParcelOnlyCanteen = window.cart.parcelOnly || false;

  const parcelFeeLabel = document.getElementById("cart-parcel-fee-label");
  if (parcelFeeLabel) parcelFeeLabel.innerText = `+ ₹${parcelRatePerItem} / item`;

  const parcelCheckbox = document.getElementById("cart-parcel-checkbox");
  if (parcelCheckbox) {
    parcelCheckbox.disabled = isParcelOnlyCanteen;
    parcelCheckbox.checked = isParcelOnlyCanteen || (window.cart.items.length > 0 && window.cart.items.every(i => (i.parcel_quantity || 0) === i.quantity));
  }

  // Cart items list in drawer
  const container = document.getElementById("cart-items-list");
  if (!container) return;

  if (window.cart.items.length === 0) {
    container.innerHTML = `
      <div class="text-center py-16 text-slate-400">
        <i data-lucide="shopping-bag" class="w-12 h-12 mx-auto mb-2 opacity-50"></i>
        <p class="text-sm font-bold">Your cart is empty</p>
        <p class="text-xs mt-1">Select a canteen and add your favorite dishes</p>
      </div>
    `;
    updateBillCalculations(0, 0, false, 0, 0);
    if (window.lucide) lucide.createIcons();
    return;
  }

  let subtotal = 0;
  let parcelItemsCount = 0;

  container.innerHTML = window.cart.items.map(it => {
    const lineTotal = it.price * it.quantity;
    subtotal += lineTotal;
    const itemParcelQty = isParcelOnlyCanteen ? it.quantity : (it.parcel_quantity || 0);
    const itemDineInQty = it.quantity - itemParcelQty;
    parcelItemsCount += itemParcelQty;

    return `
      <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2.5">
        <div class="flex items-center justify-between gap-3">
          <div class="flex items-center gap-3">
            <img src="${it.image_url || '/static/images/foods/chicken_biryani.jpg'}" class="w-12 h-12 rounded-xl object-cover" alt="${it.name}" />
            <div>
              <h4 class="font-bold text-xs text-slate-900">${it.name}</h4>
              <span class="text-xs text-slate-500">₹ ${it.price} × ${it.quantity}</span>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div class="flex items-center gap-1.5 bg-white rounded-lg p-1 border border-slate-200">
              <button onclick="decrementCartItem(${it.id})" class="w-6 h-6 rounded bg-slate-100 text-slate-800 font-black text-xs flex items-center justify-center">-</button>
              <span class="text-xs font-bold px-1">${it.quantity}</span>
              <button onclick="incrementCartItem(${it.id})" class="w-6 h-6 rounded bg-rathinam-purple text-white font-black text-xs flex items-center justify-center">+</button>
            </div>
            <span class="font-bold text-xs text-slate-900 min-w-[50px] text-right">₹ ${lineTotal}</span>
          </div>
        </div>

        <!-- Multi-Quantity Parcel vs Dine-in Controls -->
        <div class="pt-2 border-t border-slate-200/60">
          ${isParcelOnlyCanteen ? `
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-semibold text-slate-500">Service:</span>
              <span class="px-2.5 py-1 rounded-md bg-orange-100 text-orange-800 text-[10px] font-extrabold flex items-center gap-1">
                📦 Takeaway Only (+₹${parcelRatePerItem} × ${it.quantity})
              </span>
            </div>
          ` : (it.quantity === 1 ? `
            <!-- Single quantity toggle -->
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-semibold text-slate-500">Service:</span>
              <div class="inline-flex rounded-lg p-0.5 bg-slate-200/80 gap-0.5">
                <button type="button" onclick="setItemParcelStatus(${it.id}, false)" class="px-2.5 py-1 rounded-md text-[10px] font-extrabold transition flex items-center gap-1 ${itemParcelQty === 0 ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'}">
                  🍽️ Dine-in
                </button>
                <button type="button" onclick="setItemParcelStatus(${it.id}, true)" class="px-2.5 py-1 rounded-md text-[10px] font-extrabold transition flex items-center gap-1 ${itemParcelQty > 0 ? 'bg-rathinam-purple text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'}">
                  📦 Parcel (+₹${parcelRatePerItem})
                </button>
              </div>
            </div>
          ` : `
            <!-- Multi quantity granular parcel counter -->
            <div class="flex items-center justify-between gap-2">
              <div>
                <span class="text-[11px] font-bold text-slate-800 flex items-center gap-1">
                  📦 Parcel count:
                </span>
                <span class="text-[10px] text-slate-500 block">
                  ${itemParcelQty > 0 ? `<b class="text-orange-700">${itemParcelQty} Parcel</b> (+₹${itemParcelQty * parcelRatePerItem})` : '0 Parcel'} • ${itemDineInQty > 0 ? `<b class="text-slate-700">${itemDineInQty} Dine-in</b>` : '0 Dine-in'}
                </span>
              </div>
              <div class="flex items-center gap-1 bg-slate-200/90 rounded-lg p-0.5">
                <button type="button" onclick="changeItemParcelQty(${it.id}, -1)" ${itemParcelQty === 0 ? 'disabled class="w-6 h-6 rounded bg-slate-100 text-slate-400 cursor-not-allowed text-xs flex items-center justify-center"' : 'class="w-6 h-6 rounded bg-white text-slate-800 hover:bg-slate-50 shadow-sm font-bold text-xs flex items-center justify-center"'}>-</button>
                <span class="text-xs font-black px-1.5 min-w-[20px] text-center text-slate-900">${itemParcelQty}</span>
                <button type="button" onclick="changeItemParcelQty(${it.id}, 1)" ${itemParcelQty >= it.quantity ? 'disabled class="w-6 h-6 rounded bg-slate-100 text-slate-400 cursor-not-allowed text-xs flex items-center justify-center"' : 'class="w-6 h-6 rounded bg-rathinam-purple text-white hover:bg-rathinam-purple-dark shadow-sm font-bold text-xs flex items-center justify-center"'}>+</button>
              </div>
            </div>
          `)}
        </div>
      </div>
    `;
  }).join("");

  const parcelCharge = parcelItemsCount * parcelRatePerItem;
  updateBillCalculations(subtotal, parcelCharge, parcelItemsCount > 0, parcelRatePerItem, parcelItemsCount);

  // Check if cart's canteen is currently open
  const actionsContainer = document.getElementById("cart-checkout-actions");
  const cartCanteen = allCanteensData.find(c => c.id === window.cart.canteenId);
  const isCartCanteenOpen = cartCanteen ? cartCanteen.is_open : true;

  if (actionsContainer) {
    if (!isCartCanteenOpen) {
      actionsContainer.className = "space-y-2 pt-2";
      actionsContainer.innerHTML = `
        <div class="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-bold flex items-center gap-2">
          <i data-lucide="lock" class="w-4 h-4 text-rose-600 flex-shrink-0"></i>
          <span>${window.cart.canteenName || 'This canteen'} is currently closed. Cannot place order.</span>
        </div>
        <button disabled class="w-full py-3 rounded-xl bg-rose-100 border border-rose-200 text-rose-700 font-extrabold text-xs cursor-not-allowed flex items-center justify-center gap-1.5 shadow-sm">
          <i data-lucide="lock" class="w-4 h-4"></i> Canteen Closed — Cannot Place Order
        </button>
      `;
    } else {
      actionsContainer.className = "grid grid-cols-2 gap-2 pt-2";
      actionsContainer.innerHTML = `
        <button onclick="startCheckout('UPI')" class="w-full py-2.5 rounded-xl bg-rathinam-purple text-white font-extrabold text-xs hover:bg-rathinam-purple-dark transition shadow flex items-center justify-center gap-1.5">
          <i data-lucide="qr-code" class="w-4 h-4"></i> Pay via UPI
        </button>
        <button onclick="startCheckout('CASH')" class="w-full py-2.5 rounded-xl bg-slate-900 text-white font-extrabold text-xs hover:bg-slate-800 transition shadow flex items-center justify-center gap-1.5">
          <i data-lucide="banknote" class="w-4 h-4"></i> Cash at Counter
        </button>
      `;
    }
  }

  if (window.lucide) lucide.createIcons();
}

function updateBillCalculations(subtotal, parcel, isParcelActive = false, parcelRate = 10, totalQty = 0) {
  const subtotalEl = document.getElementById("cart-subtotal-val");
  const parcelEl = document.getElementById("cart-parcel-val");
  const parcelLabel = document.getElementById("cart-parcel-label");
  const totalEl = document.getElementById("cart-total-val");

  if (subtotalEl) subtotalEl.innerText = `₹ ${subtotal}`;
  if (parcelEl) parcelEl.innerText = `₹ ${parcel}`;
  if (parcelLabel) {
    if (isParcelActive && totalQty > 0) {
      parcelLabel.innerHTML = `Packaging / Parcel <span class="text-[10px] text-rathinam-purple font-bold">(${totalQty} parcel item${totalQty > 1 ? 's' : ''} × ₹${parcelRate})</span>`;
    } else {
      parcelLabel.innerText = "Packaging / Parcel";
    }
  }
  if (totalEl) totalEl.innerText = `₹ ${subtotal + parcel}`;
}

function toggleCartDrawer() {
  const drawer = document.getElementById("cart-drawer");
  if (!drawer) return;
  drawer.classList.toggle("hidden");
  updateCartUI();
}

// CHECKOUT & PAYMENT FLOW
let pendingOrderData = null;

async function startCheckout(paymentMethod) {
  if (!window.cart.items.length || !window.cart.canteenId) {
    showToast("Your cart is empty!", "error");
    return;
  }

  const cartCanteen = allCanteensData.find(c => c.id === window.cart.canteenId);
  if (cartCanteen && !cartCanteen.is_open) {
    showToast(`${window.cart.canteenName} is currently CLOSED. Cannot proceed to payment!`, "error");
    return;
  }

  const notesInput = document.getElementById("cart-notes-input");
  const notes = notesInput ? notesInput.value : "";

  // Split each item by its parcel and dine-in quantity
  const payloadItems = [];
  window.cart.items.forEach(it => {
    const isParcelOnly = window.cart.parcelOnly || false;
    const parcelQty = isParcelOnly ? it.quantity : (it.parcel_quantity || 0);
    const dineInQty = it.quantity - parcelQty;

    if (parcelQty > 0) {
      payloadItems.push({
        menu_item_id: it.id,
        quantity: parcelQty,
        is_parcel: true
      });
    }
    if (dineInQty > 0) {
      payloadItems.push({
        menu_item_id: it.id,
        quantity: dineInQty,
        is_parcel: false
      });
    }
  });

  const payload = {
    canteen_id: window.cart.canteenId,
    items: payloadItems,
    payment_method: paymentMethod,
    is_parcel: payloadItems.some(i => i.is_parcel),
    notes: notes
  };

  try {
    const res = await fetch("/api/orders", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("authToken")}`
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      showToast(err.detail || "Order failed", "error");
      return;
    }

    const orderData = await res.json();
    pendingOrderData = orderData;
    window.currentTrackedOrderId = orderData.id;

    // Reset Cart
    window.cart.items = [];
    window.cart.canteenId = null;
    window.cart.isParcel = false;
    updateCartUI();
    toggleCartDrawer();

    if (paymentMethod === "UPI") {
      openUPIModal(orderData);
    } else {
      // CASH payment -> Instant Token Generation
      showToast(`Order Placed! Token #${orderData.token_number} generated.`, "success");
      openTokenTracker(orderData);
      loadStudentOrders();
      refreshCanteens();
    }

  } catch (e) {
    console.error("Checkout error:", e);
    showToast("Failed to place order. Try again.", "error");
  }
}

function openUPIModal(order) {
  const modal = document.getElementById("upi-payment-modal");
  document.getElementById("upi-modal-amount").innerText = `₹ ${order.total_amount}`;
  document.getElementById("upi-modal-canteen").innerText = `Paying to ${order.canteen_name}`;

  // Generate dynamic QR
  const qrContainer = document.getElementById("upi-qrcode-box");
  qrContainer.innerHTML = "";
  new QRCode(qrContainer, {
    text: `upi://pay?pa=rathinamcanteen@upi&pn=RathinamCanteen&am=${order.total_amount}&cu=INR&tn=Token_${order.token_number}`,
    width: 140,
    height: 140,
    colorDark: "#501650",
    colorLight: "#ffffff"
  });

  modal.classList.remove("hidden");
}

function closeUPIModal() {
  document.getElementById("upi-payment-modal").classList.add("hidden");
}

function simulateAppPayment(appName) {
  showToast(`Simulating payment from ${appName}...`, "info");
  setTimeout(() => executeMockUPIConfirmation(), 1000);
}

async function executeMockUPIConfirmation() {
  if (!pendingOrderData) return;

  try {
    const res = await fetch("/api/payments/verify-mock-upi", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        order_id: pendingOrderData.id,
        upi_id: "student@okhdfcbank",
        app: "GPay"
      })
    });

    if (res.ok) {
      closeUPIModal();
      showToast("UPI Payment Successful! Token generated.", "success");
      
      // Fetch fresh order details & show live token tracker
      const orderRes = await fetch(`/api/orders/${pendingOrderData.id}`);
      const freshOrder = await orderRes.json();
      openTokenTracker(freshOrder);
      loadStudentOrders();
      refreshCanteens();
    }
  } catch (e) {
    console.error("Mock UPI error:", e);
  }
}

// LIVE DIGITAL TOKEN TRACKER
function openTokenTracker(order) {
  window.currentTrackedOrderId = order.id;
  activeStudentOrder = order;

  // Update Nav Badge
  const navBtn = document.getElementById("active-token-nav-btn");
  const navToken = document.getElementById("nav-token-number");
  if (navBtn && navToken) {
    navToken.innerText = order.token_number;
    if (order.status !== "COMPLETED" && order.status !== "CANCELLED") {
      navBtn.classList.remove("hidden");
    } else {
      navBtn.classList.add("hidden");
    }
  }

  // Update Tracker Modal Content
  document.getElementById("tracker-token-number").innerText = order.token_number;
  document.getElementById("tracker-order-number").innerText = `Order ID: ${order.order_number}`;
  document.getElementById("tracker-canteen-name").innerText = `${order.canteen_name}`;
  document.getElementById("tracker-queue-pos").innerText = `# ${order.queue_position || 1}`;
  document.getElementById("tracker-wait-mins").innerText = order.status === "READY_FOR_PICKUP" ? "READY NOW!" : `~ ${order.estimated_wait_time_mins || 5} mins`;
  document.getElementById("tracker-total-amount").innerText = `₹ ${order.total_amount}`;
  document.getElementById("tracker-payment-label").innerText = `${order.payment_method} (${order.payment_status})`;

  // Item List
  const itemsContainer = document.getElementById("tracker-items-list");
  itemsContainer.innerHTML = (order.items || []).map(i => `
    <div class="flex justify-between">
      <span>${i.item_name} × ${i.quantity}</span>
      <span class="font-bold">₹ ${i.subtotal}</span>
    </div>
  `).join("");

  if (order.is_parcel) {
    itemsContainer.innerHTML += `
      <div class="flex justify-between text-slate-500">
        <span>Packaging / Parcel</span>
        <span>₹ ${order.parcel_charge}</span>
      </div>
    `;
  }

  updateStepperProgress(order.status);
  document.getElementById("token-tracker-modal").classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

function updateStepperProgress(status) {
  const steps = ["step-1", "step-2", "step-3", "step-4", "step-5"];
  
  // Status mapping
  const statusLevels = {
    "ORDER_PLACED": 1,
    "PAYMENT_CONFIRMED": 2,
    "PREPARING": 3,
    "READY_FOR_PICKUP": 4,
    "COMPLETED": 5
  };

  const currentLvl = statusLevels[status] || 1;

  steps.forEach((stepId, index) => {
    const el = document.getElementById(stepId);
    if (!el) return;
    const stepNum = index + 1;
    const circle = el.querySelector(".stepper-circle");

    if (stepNum < currentLvl) {
      el.className = "flex items-center gap-3 stepper-item completed";
      circle.className = "w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs stepper-circle bg-emerald-600 text-white";
      circle.innerText = "✓";
    } else if (stepNum === currentLvl) {
      el.className = "flex items-center gap-3 stepper-item active";
      if (stepNum === 4) {
        circle.className = "w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs stepper-circle bg-emerald-500 text-white pulse-green";
        circle.innerText = "🔔";
      } else {
        circle.className = "w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs stepper-circle bg-purple-900 text-white animate-pulse";
        circle.innerText = "🍳";
      }
    } else {
      el.className = "flex items-center gap-3 stepper-item text-slate-400";
      circle.className = "w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs stepper-circle bg-slate-200 text-slate-600";
      circle.innerText = `${stepNum}`;
    }
  });
}

function openActiveTokenTracker() {
  if (activeStudentOrder) {
    openTokenTracker(activeStudentOrder);
  } else {
    loadStudentOrders();
  }
}

function closeTokenTrackerModal() {
  document.getElementById("token-tracker-modal").classList.add("hidden");
}

let studentOrdersData = [];
let studentSelectedOrderFilter = 'ALL';

async function loadStudentOrders() {
  try {
    const res = await fetch("/api/orders/user/my-orders", {
      headers: { "Authorization": `Bearer ${localStorage.getItem("authToken")}` }
    });
    if (!res.ok) return;

    studentOrdersData = await res.json();
    applyStudentOrderFilters();

    // Update active banner
    const active = studentOrdersData.find(o => o.status !== "COMPLETED" && o.status !== "CANCELLED");
    const banner = document.getElementById("active-order-banner");
    const navBtn = document.getElementById("active-token-nav-btn");

    if (active) {
      activeStudentOrder = active;
      window.currentTrackedOrderId = active.id;
      if (banner) {
        banner.classList.remove("hidden");
        document.getElementById("banner-token-badge").innerText = active.token_number;
        document.getElementById("banner-status-pill").innerText = active.status.replace(/_/g, " ");
        document.getElementById("banner-canteen-info").innerHTML = `${active.canteen_name} • Estimated ready in <span class="font-bold text-slate-900">${active.status === "READY_FOR_PICKUP" ? 'READY NOW!' : active.estimated_wait_time_mins + ' mins'}</span> (Queue #${active.queue_position})`;
      }
      if (navBtn) {
        navBtn.classList.remove("hidden");
        document.getElementById("nav-token-number").innerText = active.token_number;
      }
    } else {
      activeStudentOrder = null;
      if (banner) banner.classList.add("hidden");
      if (navBtn) navBtn.classList.add("hidden");
    }

  } catch (e) {
    console.error("Error loading orders:", e);
  }
}

function filterStudentOrders(statusFilter) {
  studentSelectedOrderFilter = statusFilter;
  document.querySelectorAll(".order-filter-pill").forEach(btn => {
    if (btn.id === `order-filter-${statusFilter}`) {
      btn.className = "order-filter-pill px-3 py-1.5 rounded-full bg-slate-900 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-sm";
    } else {
      btn.className = "order-filter-pill px-3 py-1.5 rounded-full bg-slate-100 text-slate-700 hover:bg-slate-200 text-xs font-bold transition flex items-center gap-1.5";
    }
  });
  applyStudentOrderFilters();
}

function applyStudentOrderFilters() {
  const searchTerm = (document.getElementById("student-orders-search")?.value || "").toLowerCase().trim();
  const canteenFilter = document.getElementById("student-orders-canteen-filter")?.value || "ALL";

  let filtered = [...studentOrdersData];

  // 1. Status Tab Filter
  if (studentSelectedOrderFilter === "ACTIVE") {
    filtered = filtered.filter(o => ["ORDER_PLACED", "PAYMENT_CONFIRMED", "PREPARING", "READY_FOR_PICKUP"].includes(o.status));
  } else if (studentSelectedOrderFilter === "READY") {
    filtered = filtered.filter(o => o.status === "READY_FOR_PICKUP");
  } else if (studentSelectedOrderFilter === "COMPLETED") {
    filtered = filtered.filter(o => o.status === "COMPLETED");
  } else if (studentSelectedOrderFilter === "PARCEL") {
    filtered = filtered.filter(o => o.is_parcel || (o.items || []).some(i => i.is_parcel));
  }

  // 2. Canteen Dropdown Filter
  if (canteenFilter !== "ALL") {
    filtered = filtered.filter(o => String(o.canteen_id) === String(canteenFilter));
  }

  // 3. Search Filter (Token, Dish names, Order number)
  if (searchTerm) {
    filtered = filtered.filter(o => {
      const matchToken = o.token_number?.toLowerCase().includes(searchTerm);
      const matchOrderNum = o.order_number?.toLowerCase().includes(searchTerm);
      const matchCanteen = o.canteen_name?.toLowerCase().includes(searchTerm);
      const matchItem = (o.items || []).some(i => i.item_name?.toLowerCase().includes(searchTerm));
      return matchToken || matchOrderNum || matchCanteen || matchItem;
    });
  }

  renderStudentOrdersList(filtered);
}

function renderStudentOrdersList(orders) {
  const container = document.getElementById("student-orders-list");
  if (!container) return;

  if (!orders.length) {
    container.innerHTML = `
      <div class="text-center py-16 bg-white rounded-2xl border border-slate-200">
        <i data-lucide="utensils" class="w-12 h-12 text-slate-300 mx-auto mb-2"></i>
        <p class="text-sm font-bold text-slate-800">No orders placed yet</p>
        <p class="text-xs text-slate-400 mt-1">Order your first meal from Chat Stop, Z-Cafe, Seyon, or CCT</p>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  container.innerHTML = orders.map(ord => {
    const isCompleted = ord.status === "COMPLETED";
    const statusColor = isCompleted ? "bg-slate-100 text-slate-700" : (ord.status === "READY_FOR_PICKUP" ? "bg-emerald-100 text-emerald-800 pulse-green" : "bg-purple-100 text-rathinam-purple");

    return `
      <div class="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm hover:shadow-md transition space-y-3">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-sm font-black text-rathinam-purple"># ${ord.token_number}</span>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${statusColor}">${ord.status.replace(/_/g, " ")}</span>
            </div>
            <p class="text-xs text-slate-500 font-medium mt-0.5">${ord.canteen_name} • ${new Date(ord.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
          </div>
          <div class="text-right">
            <span class="text-sm font-black text-slate-900">₹ ${ord.total_amount}</span>
            <span class="text-[10px] block text-emerald-600 font-semibold">${ord.payment_method} (${ord.payment_status})</span>
          </div>
        </div>

        <div class="text-xs text-slate-600 space-y-1">
          ${(ord.items || []).map(i => `
            <div class="flex items-center justify-between py-0.5">
              <span>• ${i.item_name} × ${i.quantity}</span>
              <div class="flex items-center gap-2">
                <span class="text-[10px] px-1.5 py-0.5 rounded font-bold ${i.is_parcel ? 'bg-orange-100 text-orange-800' : 'bg-slate-100 text-slate-600'}">${i.is_parcel ? '📦 Parcel' : '🍽️ Dine-in'}</span>
                <span class="font-semibold text-slate-900">₹${i.subtotal}</span>
              </div>
            </div>
          `).join("")}
        </div>

        <div class="flex items-center justify-between pt-2 border-t border-slate-100">
          <button onclick="openReceiptModal(${ord.id})" class="text-xs font-bold text-slate-600 hover:text-slate-900 flex items-center gap-1">
            <i data-lucide="receipt" class="w-3.5 h-3.5"></i> Digital Receipt
          </button>
          
          <div class="flex items-center gap-2">
            ${!isCompleted ? `
              <button onclick="fetchAndTrackOrder(${ord.id})" class="px-3 py-1.5 rounded-xl bg-purple-900 text-white font-bold text-xs hover:bg-purple-800 transition flex items-center gap-1">
                <i data-lucide="eye" class="w-3.5 h-3.5"></i> Live Token Progress
              </button>
            ` : `
              <button onclick="reorderPreviousOrder(${ord.id})" class="px-3 py-1.5 rounded-xl bg-rathinam-purple hover:bg-rathinam-purple-dark text-white font-bold text-xs transition flex items-center gap-1 shadow">
                <i data-lucide="repeat" class="w-3.5 h-3.5"></i> Order Again
              </button>
            `}
          </div>
        </div>
      </div>
    `;
  }).join("");

  if (window.lucide) lucide.createIcons();
}

async function fetchAndTrackOrder(orderId) {
  try {
    const res = await fetch(`/api/orders/${orderId}`);
    const order = await res.json();
    openTokenTracker(order);
  } catch (e) {
    console.error("Error fetching order:", e);
  }
}

async function reorderPreviousOrder(orderId) {
  try {
    const res = await fetch(`/api/orders/${orderId}`);
    const order = await res.json();
    
    // Open canteen menu
    await openCanteenMenu(order.canteen_id);
    
    // Add items to cart
    window.cart.items = [];
    window.cart.canteenId = order.canteen_id;
    window.cart.canteenName = order.canteen_name;
    window.cart.parcelFee = selectedCanteen ? selectedCanteen.parcel_fee : 10.0;
    window.cart.parcelOnly = selectedCanteen ? selectedCanteen.parcel_only : false;

    (order.items || []).forEach(it => {
      window.cart.items.push({
        id: it.menu_item_id,
        name: it.item_name,
        price: it.unit_price,
        quantity: it.quantity,
        image_url: null,
        is_veg: true,
        is_parcel: Boolean(it.is_parcel)
      });
    });

    updateCartUI();
    toggleCartDrawer();
    showToast("Items added to cart from previous order!", "success");
  } catch (e) {
    console.error("Reorder error:", e);
  }
}

// DIGITAL RECEIPT MODAL
async function openReceiptModal(orderId) {
  if (!orderId) return;
  try {
    const res = await fetch(`/api/orders/${orderId}`);
    const order = await res.json();

    document.getElementById("receipt-canteen-name").innerText = `${order.canteen_name}`;
    document.getElementById("receipt-datetime").innerText = new Date(order.created_at).toLocaleString();
    document.getElementById("receipt-order-id").innerText = order.order_number;
    document.getElementById("receipt-token-number").innerText = order.token_number;
    document.getElementById("receipt-student-name").innerText = `${order.student_name || 'Student'}`;
    document.getElementById("receipt-payment-method").innerText = `${order.payment_method} (${order.payment_status})`;
    const parcelCount = (order.items || []).filter(i => i.is_parcel).reduce((sum, i) => sum + i.quantity, 0);
    document.getElementById("receipt-subtotal").innerText = `₹ ${order.subtotal}`;
    document.getElementById("receipt-parcel").innerText = order.parcel_charge > 0 ? `₹ ${order.parcel_charge} (${parcelCount} parcel item${parcelCount > 1 ? 's' : ''})` : `₹ 0`;
    document.getElementById("receipt-grand-total").innerText = `₹ ${order.total_amount}`;

    const itemsTable = document.getElementById("receipt-items-table");
    itemsTable.innerHTML = (order.items || []).map(i => `
      <div class="flex items-center justify-between py-1 border-b border-slate-100 last:border-0 text-xs">
        <div>
          <span class="font-bold text-slate-900">${i.item_name} × ${i.quantity}</span>
          <span class="text-[10px] ml-1.5 px-1.5 py-0.5 rounded font-bold ${i.is_parcel ? 'bg-orange-100 text-orange-800' : 'bg-slate-100 text-slate-600'}">${i.is_parcel ? '📦 Parcel' : '🍽️ Dine-in'}</span>
        </div>
        <span class="font-semibold text-slate-900">₹ ${i.subtotal}</span>
      </div>
    `).join("");

    document.getElementById("receipt-modal").classList.remove("hidden");
    if (window.lucide) lucide.createIcons();
  } catch (e) {
    console.error("Receipt error:", e);
  }
}

function closeReceiptModal() {
  document.getElementById("receipt-modal").classList.add("hidden");
}

// GLOBAL SEARCH ACROSS CANTEENS
async function executeGlobalSearch(term) {
  if (!term || term.trim().length === 0) return;
  selectStudentTab("search");
  document.getElementById("global-search-input").value = term;

  try {
    const res = await fetch(`/api/menu/search?query=${encodeURIComponent(term)}`);
    const results = await res.json();
    renderSearchResults(results, term);
  } catch (e) {
    console.error("Search error:", e);
  }
}

function setGlobalSearch(val) {
  executeGlobalSearch(val);
}

function renderSearchResults(results, query) {
  const container = document.getElementById("search-results-container");
  if (!container) return;

  if (!results.length) {
    container.innerHTML = `
      <div class="text-center py-12 bg-white rounded-2xl border border-slate-200">
        <i data-lucide="search-x" class="w-12 h-12 text-slate-300 mx-auto mb-2"></i>
        <p class="text-sm font-bold text-slate-800">No dishes found for "${query}"</p>
        <p class="text-xs text-slate-400 mt-1">Try searching for Biryani, Rice, Noodles, or Juice</p>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  container.innerHTML = `
    <h3 class="text-sm font-extrabold text-slate-800 mb-3 flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-rathinam-purple"></span> Found ${results.length} outlets serving "${query}":
    </h3>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      ${results.map(r => `
        <div class="interactive-card bg-white rounded-2xl border border-slate-200/90 p-4 shadow-sm hover:shadow-md transition flex items-center justify-between gap-4">
          <div class="flex items-center gap-3.5">
            <img src="${r.image_url || '/static/images/foods/chicken_biryani.jpg'}" class="w-16 h-16 rounded-xl object-cover shadow-sm flex-shrink-0" alt="${r.name}" />
            <div>
              <h4 class="font-extrabold text-sm text-slate-900 leading-snug">${r.name}</h4>
              <p class="text-xs font-bold text-rathinam-purple flex items-center gap-1 mt-0.5">
                <i data-lucide="store" class="w-3 h-3 text-rathinam-orange"></i> ${r.canteen_name}
              </p>
              <div class="flex items-center gap-2 text-[10px] text-slate-500 mt-1.5 font-semibold">
                <span class="text-amber-600 font-black">⚡ ~${r.estimated_wait_mins}m wait</span>
                <span>•</span>
                <span class="${r.is_available ? 'text-emerald-600 font-extrabold' : 'text-rose-600 font-extrabold'}">${r.is_available ? 'In Stock' : 'Out of Stock'}</span>
              </div>
            </div>
          </div>
          <div class="text-right flex flex-col items-end gap-2 flex-shrink-0">
            <span class="text-base font-black text-slate-900">₹ ${r.price}</span>
            <button onclick="openCanteenMenu(${r.canteen_id})" class="px-3.5 py-1.5 rounded-xl bg-slate-900 hover:bg-rathinam-purple text-white text-xs font-extrabold transition shadow-sm">
              Order Here
            </button>
          </div>
        </div>
      `).join("")}
    </div>
  `;

  if (window.lucide) lucide.createIcons();
}

// REAL TIME WEBSOCKET UI HANDLERS
function updateLiveCrowdUI(data) {
  refreshCanteens();
}

function updateItemAvailabilityInUI(data) {
  if (selectedCanteen && selectedCanteen.id === data.canteen_id) {
    const item = currentCanteenMenuItems.find(i => i.id === data.item_id);
    if (item) item.is_available = data.is_available;
    renderCanteenMenuItems(currentCanteenMenuItems);
  }
}

function handleLiveOrderStatusUpdate(order) {
  if (window.currentUser && order.student_id === window.currentUser.id) {
    if (order.status === "READY_FOR_PICKUP") {
      playOrderReadyChime();
      showToast(`🎉 Ding! Token #${order.token_number} is READY for Pickup at ${order.canteen_name}!`, "success");
    } else {
      showToast(`Order #${order.token_number} status: ${order.status.replace(/_/g, " ")}`, "info");
    }

    if (window.currentTrackedOrderId === order.id) {
      openTokenTracker(order);
    }
    loadStudentOrders();
  }
}

async function loadCampusAnnouncements() {
  try {
    const res = await fetch("/api/announcements");
    const announcements = await res.json();
    
    // Render Home Widget
    const homeContainer = document.getElementById("home-announcements-list");
    if (homeContainer) {
      homeContainer.innerHTML = announcements.slice(0, 3).map(a => `
        <div class="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-slate-900">${a.title}</span>
            <span class="text-[10px] text-slate-400">${new Date(a.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
          </div>
          <p class="text-slate-600 leading-relaxed">${a.content}</p>
          <div class="flex items-center justify-between mt-2 pt-1 border-t border-slate-200/60 text-[10px] text-slate-400">
            <span>By ${a.author_name}</span>
            <a href="${a.whatsapp_share_url}" target="_blank" class="text-emerald-600 font-bold hover:underline flex items-center gap-1">
              <i data-lucide="share" class="w-3 h-3"></i> Share on WhatsApp
            </a>
          </div>
        </div>
      `).join("");
    }

    // Render Full List
    const fullContainer = document.getElementById("student-announcements-full-list");
    if (fullContainer) {
      fullContainer.innerHTML = announcements.map(a => `
        <div class="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm space-y-2">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-sm text-slate-900">${a.title}</h4>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${a.broadcast_type === 'CR_BROADCAST' ? 'bg-teal-100 text-teal-800' : 'bg-purple-100 text-rathinam-purple'}">${a.broadcast_type.replace(/_/g, " ")}</span>
          </div>
          <p class="text-xs text-slate-600">${a.content}</p>
          <div class="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
            <span class="text-slate-400">Posted by ${a.author_name}</span>
            <a href="${a.whatsapp_share_url}" target="_blank" class="px-3 py-1 rounded-lg bg-emerald-50 text-emerald-700 font-bold hover:bg-emerald-100 flex items-center gap-1.5 transition">
              <i data-lucide="send" class="w-3.5 h-3.5"></i> WhatsApp Share
            </a>
          </div>
        </div>
      `).join("");
    }

    if (window.lucide) lucide.createIcons();
  } catch (e) {
    console.error("Announcements error:", e);
  }
}

async function loadAIRecommendations() {
  try {
    const res = await fetch("/api/analytics/ai-predictions");
    const data = await res.json();
    const container = document.getElementById("ai-recommendations-container");
    if (!container || !data.smart_recommendations) return;

    container.innerHTML = data.smart_recommendations.map(rec => `
      <div class="rounded-2xl bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200 p-3.5 flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-rathinam-purple text-white flex items-center justify-center flex-shrink-0">
            <i data-lucide="sparkles" class="w-4 h-4 text-amber-300"></i>
          </div>
          <div>
            <h4 class="text-xs font-bold text-slate-900">${rec.title}</h4>
            <p class="text-[11px] text-slate-600 mt-0.5">${rec.message}</p>
          </div>
        </div>
        <span class="px-2.5 py-1 rounded-full bg-purple-200 text-purple-900 text-[10px] font-extrabold flex-shrink-0">
          ${rec.badge}
        </span>
      </div>
    `).join("");

    if (window.lucide) lucide.createIcons();
  } catch (e) {
    console.error("AI recommendations error:", e);
  }
}

function handleLiveCanteenStatus(data) {
  const canteen = allCanteensData.find(c => c.id === data.canteen_id);
  if (canteen) {
    canteen.is_open = data.is_open;
    if (data.active_counters) canteen.active_counters = data.active_counters;
    if (data.crowd_info) canteen.crowd_info = data.crowd_info;
  }
  renderHomeCanteenGrid(allCanteensData);
  renderAllCanteensFullGrid(allCanteensData);
  updateTopCampusCrowdStatus(allCanteensData);

  if (selectedCanteen && selectedCanteen.id === data.canteen_id) {
    selectedCanteen.is_open = data.is_open;
    openCanteenMenu(selectedCanteen.id);
  }
  updateCartUI();
  showToast(data.is_open ? `🟢 ${canteen ? canteen.name : 'Canteen'} is now OPEN!` : `🔴 ${canteen ? canteen.name : 'Canteen'} is now CLOSED by kitchen.`, data.is_open ? "success" : "warning");
}
