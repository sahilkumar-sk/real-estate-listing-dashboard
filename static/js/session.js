async function requireAuth() {
  try {
    const data = await apiFetch("/session");

    const userNameEls = document.querySelectorAll("[data-user-name]");
    userNameEls.forEach((el) => {
      el.textContent = data.user.name;
    });

    return data.user;
  } catch (error) {
    window.location.href = "/login.html";
    return null;
  }
}

async function redirectIfAuthenticated() {
  try {
    await apiFetch("/session");
    window.location.href = "/dashboard.html";
  } catch (error) {
    return null;
  }
}

async function logout() {
  try {
    await apiFetch("/logout", {
      method: "POST",
    });
  } finally {
    window.location.href = "/login.html";
  }
}
