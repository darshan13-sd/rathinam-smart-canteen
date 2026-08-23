// WebSocket Client & Real-time Broadcast Handler
let ws = null;
let wsReconnectTimer = null;

function initWebSocket(userId = null, canteenId = null) {
  if (ws) {
    try { ws.close(); } catch(e) {}
  }

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  let url = `${protocol}//${window.location.host}/ws`;
  const params = [];
  if (userId) params.push(`user_id=${userId}`);
  if (canteenId) params.push(`canteen_id=${canteenId}`);
  if (params.length > 0) url += `?${params.join('&')}`;

  ws = new WebSocket(url);

  ws.onopen = () => {
    console.log("WebSocket connected to Rathinam Smart Canteen Hub");
    if (wsReconnectTimer) {
      clearInterval(wsReconnectTimer);
      wsReconnectTimer = null;
    }
  };

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data);
      handleWebSocketEvent(msg);
    } catch (err) {
      console.error("Error parsing WebSocket message:", err);
    }
  };

  ws.onclose = () => {
    console.log("WebSocket disconnected, attempting reconnect in 3s...");
    if (!wsReconnectTimer) {
      wsReconnectTimer = setInterval(() => {
        initWebSocket(window.currentUser ? window.currentUser.id : null, window.currentUser ? window.currentUser.canteen_id : null);
      }, 3000);
    }
  };
}

function handleWebSocketEvent(msg) {
  const { type, data } = msg;
  console.log("WS Event Received:", type, data);

  switch (type) {
    case "crowd_update":
      updateLiveCrowdUI(data);
      break;

    case "item_availability_changed":
      updateItemAvailabilityInUI(data);
      break;

    case "order_status_updated":
      handleLiveOrderStatusUpdate(data);
      break;

    case "new_order":
      handleLiveNewOrderForOwner(data);
      break;

    case "new_announcement":
      handleLiveAnnouncement(data);
      break;

    case "canteen_status_update":
      handleLiveCanteenStatus(data);
      break;

    default:
      break;
  }
}

function playOrderReadyChime() {
  const audio = document.getElementById("order-ready-audio");
  if (audio) {
    audio.play().catch(e => console.log("Audio play allowed on user interaction:", e));
  }
}
