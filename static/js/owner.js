// Canteen Owner Kitchen & Live Order Queue Manager

let currentOwnerCanteenId = 1;
let ownerOrdersData = [];
let ownerMenuData = [];
let ownerSelectedStatusFilter = "ALL";

async function loadOwnerDashboard(canteenId = null) {
  if (canteenId) currentOwnerCanteenId = canteenId;
  else if (window.currentUser && window.currentUser.canteen_id) {
    currentOwnerCanteenId = window.currentUser.canteen_id;
  }

  await loadOwnerCanteenDetails();
  await loadOwnerOrders();
  await loadOwnerMenu();
}

function selectOwnerTab(tabName) {
  document.querySelectorAll(".owner-tab-btn").forEach(btn => {
    if (btn.dataset.tab === tabName) {
      btn.className = "owner-tab-btn active px-4 py-2.5 font-bold text-sm border-b-2 border-rathinam-purple text-rathinam-purple flex items-center gap-2";
    } else {
      btn.className = "owner-tab-btn px-4 py-2.5 font-bold text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-900 flex items-center gap-2";
    }
  });

  document.querySelectorAll(".owner-tab-content").forEach(el => el.classList.add("hidden"));
  const target = document.getElementById(`owner-tab-${tabName}`);
  if (target) target.classList.remove("hidden");

  if (window.lucide) lucide.createIcons();
}

async function loadOwnerCanteenDetails() {
  try {
    const res = await fetch(`/api/canteens/${currentOwnerCanteenId}`);
    const canteen = await res.json();

    document.getElementById("owner-canteen-title").innerText = `${canteen.name} — Kitchen & Order Queue`;
    document.getElementById("owner-canteen-desc").innerText = `${canteen.location || 'Campus'} • Token Prefix: ${canteen.token_prefix} • Counters: ${canteen.active_counters}`;

    const toggleBtn = document.getElementById("owner-toggle-open-btn");
    if (toggleBtn) {
      if (canteen.is_open) {
        toggleBtn.className = "px-4 py-2 rounded-xl bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-500 transition shadow";
        toggleBtn.innerText = "🟢 Canteen is OPEN";
      } else {
        toggleBtn.className = "px-4 py-2 rounded-xl bg-rose-600 text-white text-xs font-bold hover:bg-rose-500 transition shadow";
        toggleBtn.innerText = "🔴 Canteen is CLOSED";
      }
    }
  } catch (e) {
    console.error("Owner canteen details error:", e);
  }
}

async function toggleCanteenOpenStatus() {
  try {
    const res = await fetch(`/api/canteens/${currentOwnerCanteenId}`);
    const c = await res.json();
    const newStatus = !c.is_open;

    const putRes = await fetch(`/api/canteens/${currentOwnerCanteenId}/status?is_open=${newStatus}`, {
      method: "PUT",
      headers: { "Authorization": `Bearer ${localStorage.getItem("authToken")}` }
    });

    if (putRes.ok) {
      showToast(`Canteen is now ${newStatus ? 'OPEN' : 'CLOSED'}`, "info");
      loadOwnerCanteenDetails();
    }
  } catch (e) {
    console.error("Toggle error:", e);
  }
}

async function loadOwnerOrders() {
  try {
    const res = await fetch(`/api/orders/canteen/${currentOwnerCanteenId}`);
    ownerOrdersData = await res.json();
    renderOwnerMetrics(ownerOrdersData);
    renderOwnerOrdersGrid(ownerOrdersData);
  } catch (e) {
    console.error("Owner orders error:", e);
  }
}

function renderOwnerMetrics(orders) {
  const activeCount = orders.filter(o => o.status !== "COMPLETED" && o.status !== "CANCELLED").length;
  const readyCount = orders.filter(o => o.status === "READY_FOR_PICKUP").length;
  const completedCount = orders.filter(o => o.status === "COMPLETED").length;
  const revenue = orders.filter(o => o.payment_status === "PAID").reduce((sum, o) => sum + o.total_amount, 0);

  document.getElementById("owner-metric-active").innerText = activeCount;
  document.getElementById("owner-metric-ready").innerText = readyCount;
  document.getElementById("owner-metric-rev").innerText = `₹ ${revenue}`;

  const crowdEl = document.getElementById("owner-metric-crowd");
  if (activeCount <= 2) crowdEl.innerText = "LOW (~4m)";
  else if (activeCount <= 5) crowdEl.innerText = "MEDIUM (~10m)";
  else crowdEl.innerText = "HIGH (~18m)";
}

function filterOwnerOrders(status) {
  ownerSelectedStatusFilter = status;
  document.querySelectorAll(".owner-queue-filter-btn").forEach(btn => {
    if (btn.dataset.status === status) {
      btn.className = "owner-queue-filter-btn active px-3 py-1.5 rounded-lg bg-slate-900 text-white";
    } else {
      btn.className = "owner-queue-filter-btn px-3 py-1.5 rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200";
    }
  });
  renderOwnerOrdersGrid(ownerOrdersData);
}

function renderOwnerOrdersGrid(orders) {
  const container = document.getElementById("owner-orders-grid");
  if (!container) return;

  let filtered = orders;
  if (ownerSelectedStatusFilter !== "ALL") {
    filtered = orders.filter(o => o.status === ownerSelectedStatusFilter);
  }

  if (!filtered.length) {
    container.innerHTML = `
      <div class="col-span-full text-center py-12 bg-white rounded-2xl border border-slate-200">
        <i data-lucide="check-circle-2" class="w-10 h-10 text-emerald-500 mx-auto mb-2"></i>
        <p class="text-sm font-bold text-slate-800">All caught up! No orders in this filter.</p>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  container.innerHTML = filtered.map(ord => {
    const isReady = ord.status === "READY_FOR_PICKUP";
    const isPreparing = ord.status === "PREPARING";
    const isPaid = ord.payment_status === "PAID";
    const isCompleted = ord.status === "COMPLETED";

    let borderClass = "border-slate-200";
    if (isReady) borderClass = "border-emerald-400 bg-emerald-50/40 pulse-green";
    else if (isPreparing) borderClass = "border-purple-300 bg-purple-50/30";

    return `
      <div class="bg-white rounded-2xl border-2 ${borderClass} p-4 shadow-sm space-y-3">
        <!-- Top Strip -->
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <span class="text-2xl font-black text-slate-900 block leading-tight"># ${ord.token_number}</span>
            <span class="text-[10px] text-slate-500 font-mono">${ord.student_name} • ${new Date(ord.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
          </div>
          <div class="text-right">
            <span class="text-xs font-black px-2 py-0.5 rounded-full ${isPaid ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">
              ${ord.payment_method} (${ord.payment_status})
            </span>
            <span class="block text-sm font-black text-slate-900 mt-1">₹ ${ord.total_amount}</span>
          </div>
        </div>

        <!-- Food Items -->
        <div class="space-y-1.5 py-1">
          ${(ord.items || []).map(i => `
            <div class="flex items-center justify-between text-xs font-semibold text-slate-800">
              <span class="flex items-center gap-1.5">
                • ${i.item_name}
                ${i.is_parcel ? `
                  <span class="px-1.5 py-0.5 rounded bg-orange-100 text-orange-800 font-extrabold text-[9px]">📦 PARCEL</span>
                ` : `
                  <span class="px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 font-extrabold text-[9px]">🍽️ DINE-IN</span>
                `}
              </span>
              <span class="font-bold text-rathinam-purple bg-purple-50 px-2 py-0.5 rounded-md">× ${i.quantity}</span>
            </div>
          `).join("")}
          ${ord.is_parcel ? `
            <div class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-orange-100 text-orange-800 font-bold text-[10px] mt-1">
              📦 Takeaway Parcel Charge: ₹${ord.parcel_charge}
            </div>
          ` : ''}
          ${ord.notes ? `
            <div class="text-[11px] text-slate-500 italic bg-slate-50 p-2 rounded-lg border border-slate-100">
              Note: "${ord.notes}"
            </div>
          ` : ''}
        </div>

        <!-- Action Status Advancer -->
        <div class="pt-2 border-t border-slate-100 flex items-center justify-between gap-2">
          ${ord.status === "PAYMENT_CONFIRMED" || ord.status === "ORDER_PLACED" ? `
            <button onclick="advanceOrderStatus(${ord.id}, 'PREPARING')" class="w-full py-2.5 rounded-xl bg-purple-900 hover:bg-purple-800 text-white font-black text-xs transition shadow flex items-center justify-center gap-1.5">
              <i data-lucide="flame" class="w-4 h-4"></i> Start Cooking (Preparing)
            </button>
          ` : ''}

          ${ord.status === "PREPARING" ? `
            <button onclick="advanceOrderStatus(${ord.id}, 'READY_FOR_PICKUP')" class="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs transition shadow flex items-center justify-center gap-1.5 pulse-green">
              <i data-lucide="bell" class="w-4 h-4"></i> Mark READY for Pickup
            </button>
          ` : ''}

          ${ord.status === "READY_FOR_PICKUP" ? `
            <button onclick="advanceOrderStatus(${ord.id}, 'COMPLETED')" class="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-black text-xs transition shadow flex items-center justify-center gap-1.5">
              <i data-lucide="check" class="w-4 h-4"></i> Complete &amp; Handover
            </button>
          ` : ''}

          ${isCompleted ? `
            <span class="text-xs font-bold text-slate-400 py-1 flex items-center gap-1">
              <i data-lucide="check-check" class="w-4 h-4 text-emerald-500"></i> Order Completed &amp; Collected
            </span>
          ` : ''}
        </div>
      </div>
    `;
  }).join("");

  if (window.lucide) lucide.createIcons();
}

async function advanceOrderStatus(orderId, newStatus) {
  try {
    const res = await fetch(`/api/orders/${orderId}/status`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("authToken")}`
      },
      body: JSON.stringify({ status: newStatus })
    });

    if (res.ok) {
      showToast(`Order status advanced to ${newStatus.replace(/_/g, " ")}`, "success");
      loadOwnerOrders();
    }
  } catch (e) {
    console.error("Advance status error:", e);
  }
}

// OWNER MENU & STOCK SWITCH
async function loadOwnerMenu() {
  try {
    const res = await fetch(`/api/menu?canteen_id=${currentOwnerCanteenId}`);
    ownerMenuData = await res.json();
    renderOwnerMenuTable(ownerMenuData);
  } catch (e) {
    console.error("Owner menu error:", e);
  }
}

function renderOwnerMenuTable(items) {
  const container = document.getElementById("owner-menu-items-table");
  if (!container) return;

  container.innerHTML = `
    <table class="w-full text-left text-xs">
      <thead class="bg-slate-50 text-slate-500 uppercase font-bold text-[10px] tracking-wider border-b border-slate-100">
        <tr>
          <th class="py-3 px-4">Dish</th>
          <th class="py-3 px-4">Category</th>
          <th class="py-3 px-4">Price</th>
          <th class="py-3 px-4">Prep Time</th>
          <th class="py-3 px-4">Live Stock Availability</th>
          <th class="py-3 px-4 text-right">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100">
        ${items.map(item => `
          <tr class="hover:bg-slate-50/80 transition">
            <td class="py-3.5 px-4 font-bold text-slate-900 flex items-center gap-2">
              <img src="${item.image_url || '/static/images/foods/chicken_biryani.jpg'}" class="w-8 h-8 rounded-lg object-cover" />
              <div>
                <div>${item.name}</div>
                <span class="text-[10px] text-slate-400">${item.is_veg ? 'Pure Veg' : (item.is_egg ? 'Egg' : 'Non-Veg')}</span>
              </div>
            </td>
            <td class="py-3.5 px-4 text-slate-600 font-semibold">${item.category}</td>
            <td class="py-3.5 px-4 font-black text-slate-900">₹ ${item.price}</td>
            <td class="py-3.5 px-4 text-slate-600">~${item.prep_time_mins} mins</td>
            <td class="py-3.5 px-4">
              <button onclick="toggleItemStock(${item.id})" class="px-3 py-1 rounded-full text-xs font-bold transition flex items-center gap-1.5 ${item.is_available ? 'bg-emerald-100 text-emerald-800 hover:bg-emerald-200' : 'bg-rose-100 text-rose-800 hover:bg-rose-200'}">
                <span class="w-2 h-2 rounded-full ${item.is_available ? 'bg-emerald-500' : 'bg-rose-500'}"></span>
                ${item.is_available ? 'In Stock (Active)' : 'Out of Stock (Disabled)'}
              </button>
            </td>
            <td class="py-3.5 px-4 text-right">
              <button onclick="deleteMenuItem(${item.id})" class="text-rose-600 hover:text-rose-800 p-1 font-bold">
                <i data-lucide="trash-2" class="w-4 h-4"></i>
              </button>
            </td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;

  if (window.lucide) lucide.createIcons();
}

async function toggleItemStock(itemId) {
  try {
    const res = await fetch(`/api/menu/${itemId}/toggle-availability`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${localStorage.getItem("authToken")}` }
    });

    if (res.ok) {
      const data = await res.json();
      showToast(data.message, "info");
      loadOwnerMenu();
    }
  } catch (e) {
    console.error("Toggle stock error:", e);
  }
}

async function deleteMenuItem(itemId) {
  if (!confirm("Are you sure you want to remove this dish from the menu?")) return;
  try {
    const res = await fetch(`/api/menu/${itemId}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${localStorage.getItem("authToken")}` }
    });
    if (res.ok) {
      showToast("Dish removed from menu", "info");
      loadOwnerMenu();
    }
  } catch (e) {
    console.error("Delete menu item error:", e);
  }
}

// INCOMING ORDER SOUND / EVENT
function handleLiveNewOrderForOwner(order) {
  if (window.currentUser && window.currentUser.canteen_id === order.canteen_id) {
    playOrderReadyChime();
    showToast(`🔔 New Order #${order.token_number} received! (${order.items.length} items)`, "warning");
    loadOwnerOrders();
  }
}

// BROADCAST MODAL
function openBroadcastModal() {
  document.getElementById("broadcast-modal").classList.remove("hidden");
}

function closeBroadcastModal() {
  document.getElementById("broadcast-modal").classList.add("hidden");
}

async function submitBroadcastAnnouncement() {
  const title = document.getElementById("broadcast-title-input").value;
  const content = document.getElementById("broadcast-content-input").value;
  const targetClass = document.getElementById("broadcast-target-select").value;

  if (!title || !content) {
    showToast("Please enter title and content", "error");
    return;
  }

  try {
    const res = await fetch("/api/announcements", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("authToken")}`
      },
      body: JSON.stringify({
        title,
        content,
        target_class: targetClass,
        broadcast_type: "CANTEEN_UPDATE"
      })
    });

    if (res.ok) {
      closeBroadcastModal();
      showToast("Announcement published to student feed!", "success");
      document.getElementById("broadcast-title-input").value = "";
      document.getElementById("broadcast-content-input").value = "";
    }
  } catch (e) {
    console.error("Broadcast error:", e);
  }
}

// ADD DISH MODAL
function openAddDishModal() {
  document.getElementById("add-dish-modal").classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

function closeAddDishModal() {
  document.getElementById("add-dish-modal").classList.add("hidden");
}

async function submitAddNewDish() {
  const name = document.getElementById("new-dish-name").value.trim();
  const price = parseFloat(document.getElementById("new-dish-price").value);
  const prepTime = parseInt(document.getElementById("new-dish-prep").value) || 5;
  const category = document.getElementById("new-dish-category").value;
  const diet = document.getElementById("new-dish-diet").value;
  const imageUrl = document.getElementById("new-dish-image").value.trim() || "/static/images/foods/chicken_biryani.jpg";
  const desc = document.getElementById("new-dish-desc").value.trim();

  if (!name || isNaN(price) || price <= 0) {
    showToast("Please enter a valid dish name and price", "error");
    return;
  }

  const payload = {
    canteen_id: currentOwnerCanteenId,
    name: name,
    price: price,
    category: category,
    description: desc,
    is_veg: diet === "VEG",
    is_egg: diet === "EGG",
    is_available: true,
    image_url: imageUrl,
    prep_time_mins: prepTime,
    parcel_price: 10.0
  };

  try {
    const res = await fetch("/api/menu", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("authToken")}`
      },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      closeAddDishModal();
      showToast(`Added "${name}" to menu with custom photo!`, "success");
      document.getElementById("new-dish-name").value = "";
      document.getElementById("new-dish-price").value = "";
      document.getElementById("new-dish-desc").value = "";
      loadOwnerMenu();
    } else {
      const err = await res.json();
      showToast(err.detail || "Failed to add dish", "error");
    }
  } catch (e) {
    console.error("Add dish error:", e);
    showToast("Error adding dish", "error");
  }
}
