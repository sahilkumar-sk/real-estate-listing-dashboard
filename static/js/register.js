document.addEventListener("DOMContentLoaded", async () => {
  await redirectIfAuthenticated();

  const form = document.getElementById("registerForm");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      name: document.getElementById("name").value.trim(),
      email: document.getElementById("email").value.trim(),
      password: document.getElementById("password").value.trim(),
    };

    try {
      await apiFetch("/register", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      window.location.href = "/dashboard.html";
    } catch (error) {
      showMessage("registerMessage", error.message, "error");
    }
  });
});
