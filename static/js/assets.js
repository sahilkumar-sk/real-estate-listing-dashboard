let editingListingId = null;
let agentsCache = [];
let locationsCache = [];

document.addEventListener("DOMContentLoaded", async () => {
  await requireAuth();

  await loadFormOptions();
  await loadListings();

  document.getElementById("listingForm").addEventListener("submit", saveListing);
  document.getElementById("cancelEditBtn").addEventListener("click", resetListingForm);
  document.getElementById("closeShowSheetBtn").addEventListener("click", closeShowSheet);
});

async function loadFormOptions() {
  try {
    agentsCache = await apiFetch("/agents");
    locationsCache = await apiFetch("/locations");

    document.getElementById("listingAgent").innerHTML = `
      <option value="">Unassigned</option>
      ${agentsCache.map((a) => `<option value="${a.id}">${a.name} - ${a.specialization || "Agent"}</option>`).join("")}
    `;

    document.getElementById("listingLocation").innerHTML = `
      <option value="">No office selected</option>
      ${locationsCache.map((l) => `<option value="${l.id}">${l.name} - ${l.city}</option>`).join("")}
    `;
  } catch (error) {
    showMessage("listingMessage", error.message, "error");
  }
}

async function loadListings() {
  try {
    const listings = await apiFetch("/listings");
    renderListings(listings);
  } catch (error) {
    showMessage("listingMessage", error.message, "error");
  }
}

function renderListings(listings) {
  const tbody = document.getElementById("listingsBody");

  if (!listings.length) {
    tbody.innerHTML = `<tr><td colspan="9" class="empty-state">No listings found.</td></tr>`;
    return;
  }

  tbody.innerHTML = listings
    .map((listing) => `
      <tr>
        <td>
          <strong>${listing.title}</strong>
          <div class="muted">${listing.address}</div>
        </td>
        <td>${listing.city}</td>
        <td>${listing.property_type}</td>
        <td>${formatCurrency(listing.price)}</td>
        <td>${listing.bedrooms}</td>
        <td>${listing.bathrooms}</td>
        <td><span class="badge">${listing.status}</span></td>
        <td>${listing.agent_name || "Unassigned"}</td>
        <td class="actions">
          <button class="btn small" onclick="showSheet(${listing.id})">Show Sheet</button>
          <button class="btn small" onclick="editListing(${listing.id})">Edit</button>
          <button class="btn small danger" onclick="deleteListingById(${listing.id})">Delete</button>
        </td>
      </tr>
    `)
    .join("");
}

async function saveListing(event) {
  event.preventDefault();

  const payload = {
    title: document.getElementById("listingTitle").value.trim(),
    address: document.getElementById("listingAddress").value.trim(),
    city: document.getElementById("listingCity").value.trim(),
    property_type: document.getElementById("listingType").value,
    price: document.getElementById("listingPrice").value,
    bedrooms: document.getElementById("listingBedrooms").value,
    bathrooms: document.getElementById("listingBathrooms").value,
    status: document.getElementById("listingStatus").value,
    description: document.getElementById("listingDescription").value.trim(),
    agent_id: document.getElementById("listingAgent").value || null,
    location_id: document.getElementById("listingLocation").value || null,
  };

  try {
    if (editingListingId) {
      await apiFetch(`/listings/${editingListingId}`, { method: "PUT", body: JSON.stringify(payload) });
      showMessage("listingMessage", "Listing updated successfully");
    } else {
      await apiFetch("/listings", { method: "POST", body: JSON.stringify(payload) });
      showMessage("listingMessage", "Listing created successfully");
    }

    resetListingForm();
    await loadListings();
  } catch (error) {
    showMessage("listingMessage", error.message, "error");
  }
}

async function editListing(id) {
  try {
    const listing = await apiFetch(`/listings/${id}`);

    editingListingId = id;
    document.getElementById("listingTitle").value = listing.title;
    document.getElementById("listingAddress").value = listing.address;
    document.getElementById("listingCity").value = listing.city;
    document.getElementById("listingType").value = listing.property_type;
    document.getElementById("listingPrice").value = listing.price;
    document.getElementById("listingBedrooms").value = listing.bedrooms;
    document.getElementById("listingBathrooms").value = listing.bathrooms;
    document.getElementById("listingStatus").value = listing.status;
    document.getElementById("listingDescription").value = listing.description || "";
    document.getElementById("listingAgent").value = listing.agent_id || "";
    document.getElementById("listingLocation").value = listing.location_id || "";
    document.getElementById("formTitle").textContent = "Edit Listing";
    document.getElementById("saveListingBtn").textContent = "Update Listing";
    document.getElementById("cancelEditBtn").style.display = "inline-flex";
    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (error) {
    showMessage("listingMessage", error.message, "error");
  }
}

async function deleteListingById(id) {
  if (!confirm("Are you sure you want to delete this listing?")) return;

  try {
    await apiFetch(`/listings/${id}`, { method: "DELETE" });
    showMessage("listingMessage", "Listing deleted successfully");
    await loadListings();
  } catch (error) {
    showMessage("listingMessage", error.message, "error");
  }
}

async function showSheet(id) {
  try {
    const sheet = await apiFetch(`/listings/${id}/show-sheet`);

    document.getElementById("showSheetTitle").textContent = sheet.headline;
    document.getElementById("showSheetContent").innerHTML = `
      <p><strong>Address:</strong> ${sheet.address}</p>
      <p><strong>Price/Rent:</strong> ${formatCurrency(sheet.price)}</p>
      <p><strong>Type:</strong> ${sheet.property_type}</p>
      <p><strong>Beds/Baths:</strong> ${sheet.bedrooms} bed(s), ${sheet.bathrooms} bath(s)</p>
      <p><strong>Status:</strong> ${sheet.status}</p>
      <p><strong>Assigned Agent:</strong> ${sheet.assigned_agent}</p>
      <p><strong>Agent Email:</strong> ${sheet.agent_email || "-"}</p>
      <p><strong>Office:</strong> ${sheet.office}</p>
      <hr>
      <p><strong>Description:</strong></p>
      <p>${sheet.description}</p>
      <p><strong>Marketing Summary:</strong></p>
      <p>${sheet.marketing_summary}</p>
    `;

    document.getElementById("showSheetPanel").style.display = "block";
  } catch (error) {
    showMessage("listingMessage", error.message, "error");
  }
}

function closeShowSheet() {
  document.getElementById("showSheetPanel").style.display = "none";
}

function resetListingForm() {
  editingListingId = null;
  document.getElementById("listingForm").reset();
  document.getElementById("formTitle").textContent = "Add Listing";
  document.getElementById("saveListingBtn").textContent = "Save Listing";
  document.getElementById("cancelEditBtn").style.display = "none";
}
