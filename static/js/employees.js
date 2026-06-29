let editingAgentId = null;
let locationsCache = [];

document.addEventListener("DOMContentLoaded", async () => {
  await requireAuth();

  await loadLocationOptions();
  await loadAgents();

  document.getElementById("agentForm").addEventListener("submit", saveAgent);
  document.getElementById("cancelEditBtn").addEventListener("click", resetAgentForm);
});

async function loadLocationOptions() {
  try {
    locationsCache = await apiFetch("/locations");

    const select = document.getElementById("agentLocation");
    select.innerHTML = `
      <option value="">Unassigned</option>
      ${locationsCache.map((l) => `<option value="${l.id}">${l.name} - ${l.city}</option>`).join("")}
    `;
  } catch (error) {
    showMessage("agentMessage", error.message, "error");
  }
}

async function loadAgents() {
  try {
    const agents = await apiFetch("/agents");
    renderAgents(agents);
  } catch (error) {
    showMessage("agentMessage", error.message, "error");
  }
}

function renderAgents(agents) {
  const tbody = document.getElementById("agentsBody");

  if (!agents.length) {
    tbody.innerHTML = `<tr><td colspan="8" class="empty-state">No agents found.</td></tr>`;
    return;
  }

  tbody.innerHTML = agents
    .map((agent) => `
      <tr>
        <td>${agent.name}</td>
        <td>${agent.email}</td>
        <td>${agent.phone || "-"}</td>
        <td>${agent.specialization || "-"}</td>
        <td>${agent.location_name || "Unassigned"}</td>
        <td>${agent.assigned_listings || 0}</td>
        <td><span class="badge">${agent.status}</span></td>
        <td class="actions">
          <button class="btn small" onclick="editAgent(${agent.id})">Edit</button>
          <button class="btn small danger" onclick="deleteAgentById(${agent.id})">Delete</button>
        </td>
      </tr>
    `)
    .join("");
}

async function saveAgent(event) {
  event.preventDefault();

  const payload = {
    name: document.getElementById("agentName").value.trim(),
    email: document.getElementById("agentEmail").value.trim(),
    phone: document.getElementById("agentPhone").value.trim(),
    specialization: document.getElementById("agentSpecialization").value,
    location_id: document.getElementById("agentLocation").value || null,
    status: document.getElementById("agentStatus").value,
  };

  try {
    if (editingAgentId) {
      await apiFetch(`/agents/${editingAgentId}`, { method: "PUT", body: JSON.stringify(payload) });
      showMessage("agentMessage", "Agent updated successfully");
    } else {
      await apiFetch("/agents", { method: "POST", body: JSON.stringify(payload) });
      showMessage("agentMessage", "Agent created successfully");
    }

    resetAgentForm();
    await loadAgents();
  } catch (error) {
    showMessage("agentMessage", error.message, "error");
  }
}

async function editAgent(id) {
  try {
    const agent = await apiFetch(`/agents/${id}`);

    editingAgentId = id;
    document.getElementById("agentName").value = agent.name;
    document.getElementById("agentEmail").value = agent.email;
    document.getElementById("agentPhone").value = agent.phone || "";
    document.getElementById("agentSpecialization").value = agent.specialization || "";
    document.getElementById("agentLocation").value = agent.location_id || "";
    document.getElementById("agentStatus").value = agent.status;
    document.getElementById("formTitle").textContent = "Edit Agent";
    document.getElementById("saveAgentBtn").textContent = "Update Agent";
    document.getElementById("cancelEditBtn").style.display = "inline-flex";
  } catch (error) {
    showMessage("agentMessage", error.message, "error");
  }
}

async function deleteAgentById(id) {
  if (!confirm("Are you sure you want to delete this agent? Listings assigned to this agent will become unassigned.")) return;

  try {
    await apiFetch(`/agents/${id}`, { method: "DELETE" });
    showMessage("agentMessage", "Agent deleted successfully");
    await loadAgents();
  } catch (error) {
    showMessage("agentMessage", error.message, "error");
  }
}

function resetAgentForm() {
  editingAgentId = null;
  document.getElementById("agentForm").reset();
  document.getElementById("formTitle").textContent = "Add Agent";
  document.getElementById("saveAgentBtn").textContent = "Save Agent";
  document.getElementById("cancelEditBtn").style.display = "none";
}
