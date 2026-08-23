// Class Representative (CR) WhatsApp Broadcast & Crowd Radar Module

let crBroadcastMessageText = "";

async function loadCRDashboard() {
  await generateCRWhatsAppMessage();
  await loadCRCanteenRadar();
}

async function generateCRWhatsAppMessage() {
  const targetClass = document.getElementById("cr-broadcast-class").value || "ECE-A";
  const leaveTime = document.getElementById("cr-broadcast-time").value || "12:30 PM";

  try {
    const res = await fetch(`/api/announcements/generate-cr-broadcast?target_class=${encodeURIComponent(targetClass)}&leave_time=${encodeURIComponent(leaveTime)}`);
    const data = await res.json();

    crBroadcastMessageText = data.message_text;

    // Update Preview Box
    const previewEl = document.getElementById("cr-message-preview");
    if (previewEl) previewEl.innerText = data.message_text;

    // Update WhatsApp link
    const shareBtn = document.getElementById("cr-whatsapp-share-btn");
    if (shareBtn) shareBtn.href = data.whatsapp_url;

  } catch (e) {
    console.error("Error generating CR broadcast:", e);
  }
}

function copyCRWhatsAppMessage() {
  if (!crBroadcastMessageText) return;
  navigator.clipboard.writeText(crBroadcastMessageText).then(() => {
    showToast("WhatsApp broadcast message copied to clipboard!", "success");
  }).catch(() => {
    showToast("Failed to copy text", "error");
  });
}

async function postCRInAppAnnouncement() {
  const targetClass = document.getElementById("cr-broadcast-class").value || "ECE-A";
  const leaveTime = document.getElementById("cr-broadcast-time").value || "12:30 PM";

  try {
    const res = await fetch("/api/announcements", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("authToken")}`
      },
      body: JSON.stringify({
        title: `📢 ${targetClass} Canteen Advisory (${leaveTime})`,
        content: crBroadcastMessageText,
        target_class: targetClass,
        broadcast_type: "CR_BROADCAST"
      })
    });

    if (res.ok) {
      showToast(`Advisory posted to ${targetClass} students!`, "success");
    }
  } catch (e) {
    console.error("Post CR announcement error:", e);
  }
}

async function loadCRCanteenRadar() {
  try {
    const res = await fetch("/api/canteens");
    const canteens = await res.json();
    const container = document.getElementById("cr-canteen-radar-list");
    if (!container) return;

    container.innerHTML = canteens.map(c => {
      const crowd = c.crowd_info || { crowd_level: "LOW", estimated_wait_time_mins: 5, active_orders: 0 };
      let badge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">🟢 LOW</span>';
      if (crowd.crowd_level === "MEDIUM") badge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800">🟡 MEDIUM</span>';
      else if (crowd.crowd_level === "HIGH") badge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800">🔴 HIGH</span>';

      return `
        <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
          <div>
            <h4 class="font-bold text-slate-900">${c.name}</h4>
            <span class="text-[10px] text-slate-500 font-semibold">${crowd.active_orders} orders in queue</span>
          </div>
          <div class="text-right flex items-center gap-2">
            <span class="font-bold text-slate-700">~${crowd.estimated_wait_time_mins}m</span>
            ${badge}
          </div>
        </div>
      `;
    }).join("");

    if (window.lucide) lucide.createIcons();
  } catch (e) {
    console.error("CR Radar error:", e);
  }
}
