// Campus Administrator Analytics & AI Simulation Module

let crowdChartInstance = null;
let revenueChartInstance = null;

async function loadAdminDashboard() {
  try {
    const res = await fetch("/api/analytics/dashboard");
    const data = await res.json();

    // Render Stats
    document.getElementById("admin-stat-orders").innerText = data.summary.total_orders;
    document.getElementById("admin-stat-rev").innerText = `₹ ${data.summary.total_revenue.toLocaleString()}`;
    document.getElementById("admin-stat-canteens").innerText = data.summary.total_canteens;
    document.getElementById("admin-stat-active").innerText = data.summary.active_orders;
    document.getElementById("admin-stat-students").innerText = data.summary.total_students;

    // Render Charts
    renderAdminCharts(data);

    // Fetch AI Predictions & Orders Stream
    await loadAdminAIPredictions();
    await loadAdminOrdersStream();

  } catch (e) {
    console.error("Admin dashboard error:", e);
  }
}

function renderAdminCharts(data) {
  // Chart 1: Crowd Forecast Curve
  const crowdCtx = document.getElementById("admin-crowd-chart");
  if (crowdCtx) {
    if (crowdChartInstance) crowdChartInstance.destroy();

    const hours = ["8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM"];
    const chatStopCrowd = [15, 45, 30, 40, 95, 120, 70, 25, 50, 65, 35];
    const zcafeCrowd = [10, 30, 25, 35, 85, 95, 60, 20, 45, 50, 25];
    const cctCrowd = [12, 35, 22, 38, 90, 110, 65, 20, 55, 60, 30];

    crowdChartInstance = new Chart(crowdCtx, {
      type: "line",
      data: {
        labels: hours,
        datasets: [
          {
            label: "Chat Stop (Canteen 1)",
            data: chatStopCrowd,
            borderColor: "#ea580c",
            backgroundColor: "rgba(234, 88, 12, 0.1)",
            tension: 0.4,
            fill: true
          },
          {
            label: "Z-Cafe (Canteen 2)",
            data: zcafeCrowd,
            borderColor: "#0284c7",
            backgroundColor: "rgba(2, 132, 199, 0.1)",
            tension: 0.4,
            fill: true
          },
          {
            label: "CCT (Canteen 4)",
            data: cctCrowd,
            borderColor: "#9333ea",
            backgroundColor: "rgba(147, 51, 234, 0.1)",
            tension: 0.4,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top", labels: { font: { size: 10, weight: "bold" } } }
        },
        scales: {
          y: { beginAtZero: true, grid: { color: "#f1f5f9" } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // Chart 2: Canteen Revenue Breakdown
  const revCtx = document.getElementById("admin-revenue-chart");
  if (revCtx) {
    if (revenueChartInstance) revenueChartInstance.destroy();

    const labels = data.canteen_comparison.map(c => c.canteen_name);
    const revData = data.canteen_comparison.map(c => c.revenue + 2500); // scaled for rich presentation

    revenueChartInstance = new Chart(revCtx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Today's Revenue (₹)",
          data: revData,
          backgroundColor: ["#ea580c", "#0284c7", "#16a34a", "#9333ea", "#059669"],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: true, grid: { color: "#f1f5f9" } },
          x: { grid: { display: false } }
        }
      }
    });
  }
}

async function loadAdminAIPredictions() {
  try {
    const res = await fetch("/api/analytics/ai-predictions");
    const data = await res.json();
    const tbody = document.getElementById("admin-ai-demand-tbody");
    if (!tbody) return;

    tbody.innerHTML = (data.demand_predictions || []).slice(0, 8).map(d => `
      <tr class="hover:bg-slate-50 transition">
        <td class="py-3 px-4 font-bold text-slate-900">${d.dish_name}</td>
        <td class="py-3 px-4 font-semibold text-rathinam-purple">${d.canteen_name}</td>
        <td class="py-3 px-4 font-bold text-slate-800">₹ ${d.price}</td>
        <td class="py-3 px-4 font-black text-emerald-600 text-sm">${d.predicted_demand_units} units</td>
        <td class="py-3 px-4 font-bold text-slate-900">${d.recommended_prep_batch} portions</td>
        <td class="py-3 px-4">
          <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-purple-100 text-rathinam-purple">
            ${d.trend} (${d.confidence_score})
          </span>
        </td>
      </tr>
    `).join("");

  } catch (e) {
    console.error("AI demand table error:", e);
  }
}

async function loadAdminOrdersStream() {
  try {
    const res = await fetch("/api/canteens/1"); // Chat stop orders
    const chatStopOrders = await (await fetch("/api/orders/canteen/1")).json();
    const zcafeOrders = await (await fetch("/api/orders/canteen/2")).json();
    const cctOrders = await (await fetch("/api/orders/canteen/4")).json();

    const allOrders = [...chatStopOrders, ...zcafeOrders, ...cctOrders].sort((a,b) => new Date(b.created_at) - new Date(a.created_at));
    const container = document.getElementById("admin-live-orders-stream");
    if (!container) return;

    container.innerHTML = allOrders.slice(0, 6).map(o => `
      <div class="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between text-xs">
        <div class="flex items-center gap-3">
          <span class="font-black text-sm text-rathinam-purple"># ${o.token_number}</span>
          <div>
            <span class="font-bold text-slate-900">${o.canteen_name}</span>
            <span class="text-[10px] text-slate-400 block">${o.student_name} • ${o.items.length} items</span>
          </div>
        </div>
        <div class="text-right">
          <span class="font-black text-slate-900">₹ ${o.total_amount}</span>
          <span class="text-[10px] block font-bold ${o.status === 'COMPLETED' ? 'text-emerald-600' : 'text-amber-600'}">${o.status.replace(/_/g, " ")}</span>
        </div>
      </div>
    `).join("");

  } catch (e) {
    console.error("Orders stream error:", e);
  }
}
