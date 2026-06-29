document.addEventListener("DOMContentLoaded", async () => {
  await requireAuth();
  await loadDashboard();
});

async function loadDashboard() {
  try {
    const stats = await apiFetch("/dashboard/stats");

    document.getElementById("totalListings").textContent = stats.total_listings;
    document.getElementById("availableListings").textContent = stats.available_listings;
    document.getElementById("pendingListings").textContent = stats.pending_listings;
    document.getElementById("rentedListings").textContent = stats.rented_listings;
    document.getElementById("soldListings").textContent = stats.sold_listings;
    document.getElementById("activeAgents").textContent = stats.active_agents;
    document.getElementById("totalLocations").textContent = stats.total_locations;
    document.getElementById("unassignedListings").textContent = stats.unassigned_listings;

    renderRecentListings(stats.recent_listings || []);
  } catch (error) {
    showMessage("dashboardMessage", error.message, "error");
  }
}

function renderRecentListings(listings) {
  const tbody = document.getElementById("recentListingsBody");

  if (!listings.length) {
    tbody.innerHTML = `<tr><td colspan="6" class="empty-state">No recent listings found.</td></tr>`;
    return;
  }

  tbody.innerHTML = listings
    .map((listing) => `
      <tr>
        <td>${listing.title}</td>
        <td>${listing.city}</td>
        <td>${listing.property_type}</td>
        <td>${formatCurrency(listing.price)}</td>
        <td><span class="badge">${listing.status}</span></td>
        <td>${listing.agent_name || "Unassigned"}</td>
      </tr>
    `)
    .join("");
}
