// Rathinam Smart Canteen Hub - Main Application & Authentication Manager

window.currentUser = null;
window.currentRole = 'STUDENT';
window.currentView = 'student';
window.currentTrackedOrderId = null;

document.addEventListener("DOMContentLoaded", async () => {
  if (window.lucide) {
    lucide.createIcons();
  }

  // Check if token exists in localStorage or load default demo session
  const token = localStorage.getItem("authToken");
  if (token) {
    try {
      const res = await fetch("/api/auth/me", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const user = await res.json();
        applyUserSession(user);
        initWebSocket(user.id, user.canteen_id);
        return;
      }
    } catch (e) {
      console.warn("Session check failed, falling back to login:", e);
    }
  }

  // Initialize with Darshan demo account
  await executeLoginWithCredentials("darshan", "password123", true);
  initWebSocket();
});

// AUTHENTICATION & SECURE SWITCH MODAL FUNCTIONS
function openAuthModal(targetUsername = null) {
  const modal = document.getElementById("auth-modal");
  const errorBanner = document.getElementById("auth-error-banner");
  if (errorBanner) errorBanner.classList.add("hidden");

  const pwdInput = document.getElementById("auth-password-input");
  if (pwdInput) {
    pwdInput.value = "";
    pwdInput.type = "password";
  }

  const eyeIcon = document.getElementById("password-eye-icon");
  if (eyeIcon) eyeIcon.setAttribute("data-lucide", "eye");

  if (targetUsername) {
    const selectEl = document.getElementById("auth-account-select");
    if (selectEl) selectEl.value = targetUsername;
    handleAccountSelection(targetUsername);
  } else if (window.currentUser) {
    const selectEl = document.getElementById("auth-account-select");
    if (selectEl) selectEl.value = window.currentUser.username;
    handleAccountSelection(window.currentUser.username);
  }

  if (modal) modal.classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
  if (pwdInput) pwdInput.focus();
}

function closeAuthModal() {
  const modal = document.getElementById("auth-modal");
  if (modal) modal.classList.add("hidden");
}

function handleAccountSelection(username) {
  const usernameInput = document.getElementById("auth-username-input");
  const pwdHint = document.getElementById("auth-password-hint");
  const errorBanner = document.getElementById("auth-error-banner");
  if (errorBanner) errorBanner.classList.add("hidden");

  if (usernameInput) usernameInput.value = username;
  if (pwdHint) {
    if (username === "admin") {
      pwdHint.innerText = "Password: admin123";
    } else {
      pwdHint.innerText = "Password: password123";
    }
  }
}

function fillPassword(pwd) {
  const pwdInput = document.getElementById("auth-password-input");
  if (pwdInput) pwdInput.value = pwd;
}

function togglePasswordVisibility() {
  const pwdInput = document.getElementById("auth-password-input");
  const eyeIcon = document.getElementById("password-eye-icon");
  if (!pwdInput) return;

  if (pwdInput.type === "password") {
    pwdInput.type = "text";
    if (eyeIcon) eyeIcon.setAttribute("data-lucide", "eye-off");
  } else {
    pwdInput.type = "password";
    if (eyeIcon) eyeIcon.setAttribute("data-lucide", "eye");
  }
  if (window.lucide) lucide.createIcons();
}

async function submitLogin() {
  const usernameInput = document.getElementById("auth-username-input");
  const passwordInput = document.getElementById("auth-password-input");
  const errorBanner = document.getElementById("auth-error-banner");
  const errorMsg = document.getElementById("auth-error-msg");
  const submitBtn = document.getElementById("auth-submit-btn");

  const username = usernameInput ? usernameInput.value.trim() : "";
  const password = passwordInput ? passwordInput.value : "";

  if (!username || !password) {
    if (errorBanner && errorMsg) {
      errorMsg.innerText = "Please enter both username and password.";
      errorBanner.classList.remove("hidden");
    }
    return;
  }

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="animate-spin mr-2">⏳</span> Verifying Password...`;
  }

  try {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) {
      const err = await res.json();
      if (errorBanner && errorMsg) {
        errorMsg.innerText = err.detail || "Incorrect password! Access denied.";
        errorBanner.classList.remove("hidden");
      }
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<i data-lucide="key" class="w-4 h-4"></i> Verify Password & Log In`;
        if (window.lucide) lucide.createIcons();
      }
      return;
    }

    const data = await res.json();
    localStorage.setItem("authToken", data.access_token);
    applyUserSession(data.user);
    closeAuthModal();
    initWebSocket(data.user.id, data.user.canteen_id);
    showToast(`Authentication verified! Logged in as ${data.user.full_name}`, "success");

  } catch (e) {
    console.error("Login request error:", e);
    if (errorBanner && errorMsg) {
      errorMsg.innerText = "Connection error. Please try again.";
      errorBanner.classList.remove("hidden");
    }
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<i data-lucide="key" class="w-4 h-4"></i> Verify Password & Log In`;
      if (window.lucide) lucide.createIcons();
    }
  }
}

async function executeLoginWithCredentials(username, password, silent = false) {
  try {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem("authToken", data.access_token);
      applyUserSession(data.user);
      if (!silent) showToast(`Logged in as ${data.user.full_name}`, "success");
    }
  } catch (e) {
    console.error("Auto login error:", e);
  }
}

function applyUserSession(user) {
  window.currentUser = user;
  window.currentRole = user.role;

  // Update Top Navbar Profile Pill
  updateUserProfileNavbar(user);

  // Switch view based on role
  if (user.role === "CANTEEN_OWNER") {
    switchView("owner");
    loadOwnerDashboard(user.canteen_id);
  } else if (user.role === "CLASS_REP") {
    switchView("cr");
    loadCRDashboard();
  } else if (user.role === "ADMIN") {
    switchView("admin");
    loadAdminDashboard();
  } else {
    switchView("student");
    loadStudentDashboard();
  }
}

function updateUserProfileNavbar(user) {
  const nameEl = document.getElementById("nav-user-fullname");
  const roleEl = document.getElementById("nav-user-role-badge");
  const initialsEl = document.getElementById("user-avatar-initials");
  const greeting = document.getElementById("student-greeting-name");

  if (greeting) greeting.innerText = user.full_name.split(" ")[0];

  if (nameEl) nameEl.innerText = user.full_name;
  if (initialsEl) initialsEl.innerText = user.full_name.charAt(0).toUpperCase();

  if (roleEl) {
    if (user.role === "STUDENT") {
      roleEl.innerText = `Student (${user.department || 'Campus'})`;
      roleEl.className = "block leading-tight text-[10px] text-rathinam-purple font-semibold";
    } else if (user.role === "CANTEEN_OWNER") {
      roleEl.innerText = `Canteen Owner`;
      roleEl.className = "block leading-tight text-[10px] text-amber-600 font-bold";
    } else if (user.role === "CLASS_REP") {
      roleEl.innerText = `Class Rep (${user.department || 'CR'})`;
      roleEl.className = "block leading-tight text-[10px] text-teal-600 font-bold";
    } else if (user.role === "ADMIN") {
      roleEl.innerText = `Campus Admin`;
      roleEl.className = "block leading-tight text-[10px] text-rose-600 font-bold";
    }
  }

  if (window.lucide) lucide.createIcons();
}

function logoutUser() {
  localStorage.removeItem("authToken");
  window.currentUser = null;
  showToast("Logged out safely. Please authenticate to continue.", "info");
  openAuthModal("darshan");
}

function switchView(viewName) {
  window.currentView = viewName;
  document.querySelectorAll(".view-section").forEach(el => el.classList.add("hidden"));

  const target = document.getElementById(`${viewName}-view`);
  if (target) target.classList.remove("hidden");

  // Show/Hide bottom nav for mobile (only for student)
  const bottomBar = document.getElementById("mobile-bottom-bar");
  if (bottomBar) {
    if (viewName === "student") {
      bottomBar.classList.remove("hidden");
    } else {
      bottomBar.classList.add("hidden");
    }
  }

  if (window.lucide) lucide.createIcons();
}

function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  let bgClass = "bg-slate-900 text-white";
  let icon = "info";

  if (type === "success") {
    bgClass = "bg-emerald-600 text-white";
    icon = "check-circle";
  } else if (type === "error") {
    bgClass = "bg-rose-600 text-white";
    icon = "alert-circle";
  } else if (type === "warning") {
    bgClass = "bg-amber-500 text-slate-900";
    icon = "alert-triangle";
  }

  toast.className = `p-4 rounded-2xl shadow-xl flex items-center gap-3 text-xs font-bold pointer-events-auto transform transition-all duration-300 translate-y-2 opacity-0 ${bgClass}`;
  toast.innerHTML = `
    <i data-lucide="${icon}" class="w-5 h-5 flex-shrink-0"></i>
    <div class="flex-1">${message}</div>
  `;

  container.appendChild(toast);
  if (window.lucide) lucide.createIcons();

  requestAnimationFrame(() => {
    toast.classList.remove("translate-y-2", "opacity-0");
  });

  setTimeout(() => {
    toast.classList.add("opacity-0", "translate-x-full");
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
