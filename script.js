const BAND_CATEGORIES = ["Estudio", "Vivo", "Recopilatorio", "Single/EP", "Bootleg", "Box"];
const SOLO_CATEGORIES = ["Estudio", "Vivo", "Box"];
const FORMAT_OPTIONS = ["Vinilo", "CD", "Digital", "Cassette", "DVD", "Blu-ray"];

const db = firebase.firestore();
const collectionRef = db.collection("coleccion");

let state = {};
let currentView = "band"; // "band" | "solo"
let currentFilters = new Set(); // vacío = "Todos"
let currentArtist = "all";
let searchTerm = "";
let onlyMissing = false;

const tbody = document.getElementById("album-body");
const thead = document.getElementById("table-head");
const searchInput = document.getElementById("search");
const onlyMissingCheckbox = document.getElementById("only-missing");
const filterTabsEl = document.getElementById("filter-tabs");
const artistSelect = document.getElementById("artist-select");
const viewTabs = document.querySelectorAll(".view-tab");

function getEntry(id) {
  const raw = state[id] || {};
  // Compatibilidad con datos viejos: antes "format" era un string único.
  const formats = Array.isArray(raw.formats) ? raw.formats : raw.format ? [raw.format] : [];
  return { owned: !!raw.owned, formats, notes: raw.notes || "" };
}

function updateEntry(id, patch) {
  const entry = { ...getEntry(id), ...patch };
  state[id] = entry;
  renderStats();
  collectionRef.doc(id).set(entry, { merge: true }).catch((err) => {
    console.error("No se pudo guardar en la nube:", err);
  });
}

function toggleFormat(id, formatValue, checked) {
  const current = getEntry(id).formats;
  const next = checked ? [...current, formatValue] : current.filter((f) => f !== formatValue);
  updateEntry(id, { formats: next });
}

function albumsInView() {
  if (currentView === "band") {
    return ALL_ALBUMS.filter((a) => a.artist === "The Rolling Stones");
  }
  return ALL_ALBUMS.filter(
    (a) => a.artist !== "The Rolling Stones" && (currentArtist === "all" || a.artist === currentArtist)
  );
}

function matchesFilters(album) {
  if (currentFilters.size > 0 && !currentFilters.has(album.category)) return false;
  if (searchTerm && !album.title.toLowerCase().includes(searchTerm)) return false;
  if (onlyMissing && getEntry(album.id).owned) return false;
  return true;
}

function renderStats() {
  const rows = albumsInView().filter(matchesFilters);
  const total = rows.length;
  const owned = rows.filter((a) => getEntry(a.id).owned).length;
  const missing = total - owned;
  const pct = total ? Math.round((owned / total) * 100) : 0;

  document.getElementById("stat-total").textContent = total;
  document.getElementById("stat-owned").textContent = owned;
  document.getElementById("stat-missing").textContent = missing;
  document.getElementById("stat-pct").textContent = `${pct}%`;
}

function renderFilterTabs() {
  const categories = currentView === "band" ? BAND_CATEGORIES : SOLO_CATEGORIES;
  filterTabsEl.innerHTML = "";

  const todosBtn = document.createElement("button");
  todosBtn.className = "tab" + (currentFilters.size === 0 ? " active" : "");
  todosBtn.textContent = "Todos";
  todosBtn.addEventListener("click", () => {
    currentFilters.clear();
    renderFilterTabs();
    renderTable();
  });
  filterTabsEl.appendChild(todosBtn);

  for (const cat of categories) {
    const btn = document.createElement("button");
    btn.className = "tab" + (currentFilters.has(cat) ? " active" : "");
    btn.textContent = cat === "Recopilatorio" ? "Recopilatorios" : cat;
    btn.addEventListener("click", () => {
      if (currentFilters.has(cat)) {
        currentFilters.delete(cat);
      } else {
        currentFilters.add(cat);
      }
      renderFilterTabs();
      renderTable();
    });
    filterTabsEl.appendChild(btn);
  }
}

function renderArtistSelect() {
  if (currentView !== "solo") {
    artistSelect.hidden = true;
    return;
  }
  artistSelect.hidden = false;
  artistSelect.innerHTML = `<option value="all">Todos los solistas</option>`;
  for (const artist of SOLO_ARTISTS) {
    const opt = document.createElement("option");
    opt.value = artist;
    opt.textContent = artist;
    if (artist === currentArtist) opt.selected = true;
    artistSelect.appendChild(opt);
  }
}

function renderTableHead() {
  const showArtistCol = currentView === "solo" && currentArtist === "all";
  const showRegionLabelCols = currentView === "band";

  thead.innerHTML = `
    <tr>
      <th></th>
      <th>Año</th>
      ${showArtistCol ? "<th>Artista</th>" : ""}
      <th>Álbum</th>
      <th>Tipo</th>
      ${showRegionLabelCols ? "<th>Región</th><th>Sello</th>" : ""}
      <th>Formato</th>
      <th>Notas</th>
    </tr>
  `;
}

function renderTable() {
  renderTableHead();
  tbody.innerHTML = "";

  const showArtistCol = currentView === "solo" && currentArtist === "all";
  const showRegionLabelCols = currentView === "band";
  const colSpan = 5 + (showArtistCol ? 1 : 0) + (showRegionLabelCols ? 2 : 0);

  const rows = albumsInView()
    .filter(matchesFilters)
    .sort((a, b) => a.year - b.year || a.title.localeCompare(b.title));

  if (rows.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="${colSpan}" class="empty-row">No hay álbumes que coincidan (o esta categoría todavía se está completando).</td>`;
    tbody.appendChild(tr);
    renderStats();
    return;
  }

  for (const albumRow of rows) {
    const entry = getEntry(albumRow.id);
    const tr = document.createElement("tr");
    if (entry.owned) tr.classList.add("owned-row");

    const catClass = albumRow.category.replace("/", "");

    tr.innerHTML = `
      <td>
        <input type="checkbox" ${entry.owned ? "checked" : ""} data-id="${albumRow.id}" data-field="owned" />
      </td>
      <td>${albumRow.year}</td>
      ${showArtistCol ? `<td>${albumRow.artist}</td>` : ""}
      <td>
        ${albumRow.title}
        ${albumRow.note ? `<div class="row-note">${albumRow.note}</div>` : ""}
      </td>
      <td><span class="badge badge-${catClass}">${albumRow.category}</span></td>
      ${showRegionLabelCols ? `<td>${albumRow.region || "—"}</td><td>${albumRow.label || "—"}</td>` : ""}
      <td>
        <div class="format-group">
          ${FORMAT_OPTIONS.map(
            (fmt) => `
            <label class="format-chip">
              <input type="checkbox" data-id="${albumRow.id}" data-role="format" data-value="${fmt}" ${entry.formats.includes(fmt) ? "checked" : ""} />
              ${fmt}
            </label>`
          ).join("")}
        </div>
      </td>
      <td>
        <input type="text" class="notes-input" placeholder="Notas..." value="${entry.notes || ""}" data-id="${albumRow.id}" data-field="notes" />
      </td>
    `;
    tbody.appendChild(tr);
  }

  renderStats();
}

tbody.addEventListener("change", (e) => {
  const target = e.target;
  const id = target.dataset.id;

  if (target.dataset.role === "format") {
    toggleFormat(id, target.dataset.value, target.checked);
    return;
  }

  const field = target.dataset.field;
  if (!id || !field) return;

  const value = field === "owned" ? target.checked : target.value;
  updateEntry(id, { [field]: value });
  if (field === "owned") renderTable();
});

searchInput.addEventListener("input", (e) => {
  searchTerm = e.target.value.trim().toLowerCase();
  renderTable();
});

onlyMissingCheckbox.addEventListener("change", (e) => {
  onlyMissing = e.target.checked;
  renderTable();
});

artistSelect.addEventListener("change", (e) => {
  currentArtist = e.target.value;
  renderTable();
});

viewTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    viewTabs.forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    currentView = tab.dataset.view;
    currentFilters.clear();
    currentArtist = "all";
    renderArtistSelect();
    renderFilterTabs();
    renderTable();
  });
});

renderArtistSelect();
renderFilterTabs();
tbody.innerHTML = `<tr><td class="empty-row">Conectando con la nube...</td></tr>`;

collectionRef.onSnapshot(
  (snapshot) => {
    snapshot.docChanges().forEach((change) => {
      if (change.type === "removed") {
        delete state[change.doc.id];
      } else {
        state[change.doc.id] = change.doc.data();
      }
    });
    renderTable();
  },
  (err) => {
    console.error("Error de conexión con Firestore:", err);
    tbody.innerHTML = `<tr><td class="empty-row">No se pudo conectar con la base de datos en la nube. Revisá tu conexión a internet.</td></tr>`;
  }
);

const versionEl = document.getElementById("app-version");
if (versionEl) versionEl.textContent = APP_VERSION;
