const API_BASE_URL = window.location.origin;

async function apiFetch(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let data = null;

  try {
    data = await response.json();
  } catch (error) {
    data = {};
  }

  if (!response.ok) {
    const message = data.error || data.message || "Something went wrong";
    throw new Error(message);
  }

  return data;
}

function formatCurrency(value) {
  const number = Number(value || 0);

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(number);
}

function showMessage(elementId, message, type = "success") {
  const el = document.getElementById(elementId);

  if (!el) return;

  el.textContent = message;
  el.className = `message ${type}`;
  el.style.display = "block";

  setTimeout(() => {
    el.style.display = "none";
  }, 3500);
}
