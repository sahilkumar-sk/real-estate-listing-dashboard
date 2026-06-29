document.addEventListener("DOMContentLoaded", async () => {
  await redirectIfAuthenticated();

  const form = document.getElementById("loginForm");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      email: document.getElementById("email").value.trim(),
      password: document.getElementById("password").value.trim(),
    };

    try {
      await apiFetch("/login", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      window.location.href = "/dashboard.html";
    } catch (error) {
      showMessage("loginMessage", error.message, "error");
    }
  });
});
