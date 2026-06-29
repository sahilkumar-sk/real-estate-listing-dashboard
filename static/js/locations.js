let editingLocationId = null;

document.addEventListener("DOMContentLoaded", async () => {
  await requireAuth();
  await loadLocations();

  document.getElementById("locationForm").addEventListener("submit", saveLocation);
  document.getElementById("cancelEditBtn").addEventListener("click", resetLocationForm);
});

async function loadLocations() {
  try {
    const locations = await apiFetch("/locations");
    renderLocations(locations);
  } catch (error) {
    showMessage("locationMessage", error.message, "error");
  }
}

function renderLocations(locations) {
  const tbody = document.getElementById("locationsBody");

  if (!locations.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="empty-state">No offices found.</td></tr>`;
    return;
  }

  tbody.innerHTML = locations
    .map((location) => `
      <tr>
        <td>${location.name}</td>
        <td>${location.city}</td>
        <td>${location.address || "-"}</td>
        <td><span class="badge">${location.status}</span></td>
        <td>${location.total_agents || 0}</td>
        <td>${location.total_listings || 0}</td>
        <td class="actions">
          <button class="btn small" onclick="editLocation(${location.id})">Edit</button>
          <button class="btn small danger" onclick="deleteLocationById(${location.id})">Delete</button>
        </td>
      </tr>
    `)
    .join("");
}

async function saveLocation(event) {
  event.preventDefault();

  const payload = {
    name: document.getElementById("locationName").value.trim(),
    city: document.getElementById("locationCity").value.trim(),
    address: document.getElementById("locationAddress").value.trim(),
    status: document.getElementById("locationStatus").value,
  };

  try {
    if (editingLocationId) {
      await apiFetch(`/locations/${editingLocationId}`, { method: "PUT", body: JSON.stringify(payload) });
      showMessage("locationMessage", "Office updated successfully");
    } else {
      await apiFetch("/locations", { method: "POST", body: JSON.stringify(payload) });
      showMessage("locationMessage", "Office created successfully");
    }

    resetLocationForm();
    await loadLocations();
  } catch (error) {
    showMessage("locationMessage", error.message, "error");
  }
}

async function editLocation(id) {
  try {
    const location = await apiFetch(`/locations/${id}`);

    editingLocationId = id;
    document.getElementById("locationName").value = location.name;
    document.getElementById("locationCity").value = location.city;
    document.getElementById("locationAddress").value = location.address || "";
    document.getElementById("locationStatus").value = location.status;
    document.getElementById("formTitle").textContent = "Edit Office";
    document.getElementById("saveLocationBtn").textContent = "Update Office";
    document.getElementById("cancelEditBtn").style.display = "inline-flex";
  } catch (error) {
    showMessage("locationMessage", error.message, "error");
  }
}

async function deleteLocationById(id) {
  if (!confirm("Are you sure you want to delete this office?")) return;

  try {
    await apiFetch(`/locations/${id}`, { method: "DELETE" });
    showMessage("locationMessage", "Office deleted successfully");
    await loadLocations();
  } catch (error) {
    showMessage("locationMessage", error.message, "error");
  }
}

function resetLocationForm() {
  editingLocationId = null;
  document.getElementById("locationForm").reset();
  document.getElementById("formTitle").textContent = "Add Office";
  document.getElementById("saveLocationBtn").textContent = "Save Office";
  document.getElementById("cancelEditBtn").style.display = "none";
}
