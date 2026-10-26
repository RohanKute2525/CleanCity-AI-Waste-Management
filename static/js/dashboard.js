
"use strict";

let wasteChart = null;

const $ = (id) => document.getElementById(id);

function display(id, value) {
  const element = $(id);
  if (element) element.textContent = value ?? "—";
}

function formatNumber(value) {
  return new Intl.NumberFormat().format(Number(value) || 0);
}

function renderTable(id, rows, columns, emptyMessage) {
  const body = $(id);
  if (!body) return;

  body.replaceChildren();

  if (!Array.isArray(rows) || rows.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = columns.length;
    cell.textContent = emptyMessage;
    row.appendChild(cell);
    body.appendChild(row);
    return;
  }

  rows.forEach((item) => {
    const row = document.createElement("tr");

    columns.forEach((column) => {
      const cell = document.createElement("td");
      let value = item[column.key];

      if (column.format) value = column.format(value);
      cell.textContent = value == null || value === "" ? "—" : String(value);
      row.appendChild(cell);
    });

    body.appendChild(row);
  });
}

function updateChart(items) {
  const canvas = $("wasteChart");
  const empty = $("chartEmpty");
  if (!canvas || typeof Chart === "undefined") return;

  if (!items || items.length === 0) {
    if (wasteChart) {
      wasteChart.destroy();
      wasteChart = null;
    }
    canvas.hidden = true;
    if (empty) empty.hidden = false;
    return;
  }

  canvas.hidden = false;
  if (empty) empty.hidden = true;

  if (wasteChart) wasteChart.destroy();

  wasteChart = new Chart(canvas, {
    type: "bar",
    data: {
      labels: items.map(item => item.label),
      datasets: [{
        label: "Detections",
        data: items.map(item => Number(item.count) || 0),
        backgroundColor: "#19865e",
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        y: {
          beginAtZero: true,
          ticks: { precision: 0 },
          grid: { color: "#edf1ee" }
        }
      }
    }
  });
}

async function refreshDashboard() {
  const connection = $("connection");

  try {
    const response = await fetch("/api/dashboard", {
      cache: "no-store"
    });

    if (!response.ok) {
      throw new Error("Dashboard API returned " + response.status);
    }

    const data = await response.json();

    [
      "total_detections",
      "total_bins",
      "critical_bins",
      "high_risk_hotspots",
      "total_complaints",
      "route_stops",
      "total_zones"
    ].forEach(key => display(key, formatNumber(data[key])));

    display("last_updated", data.last_updated);
    display("footerTime", "Last refresh: " + data.last_updated);

    const yolo = data.yolo_model_loaded;
    const hotspot = data.hotspot_model_loaded;

    display("yoloStatus", "YOLO: " + (yolo ? "Loaded" : "Not loaded"));
    display("hotspotStatus",
      "Hotspot model: " + (hotspot ? "Loaded" : "Not loaded"));
    display("healthYolo", yolo ? "Loaded" : "Not loaded");
    display("healthHotspot", hotspot ? "Loaded" : "Not loaded");

    if (connection) {
      connection.textContent = "● Connected";
      connection.classList.add("connected");
      connection.classList.remove("disconnected");
    }

    updateChart(data.waste_by_class);

    renderTable("detectionsTable", data.recent_detections, [
      {
        key: "timestamp",
        format: value => value ? String(value).replace("T", " ") : "—"
      },
      { key: "class_name" },
      { key: "confidence", format: value => value == null ? "—" : value + "%" }
    ], "No saved detections yet.");

    renderTable("complaintsTable", data.recent_complaints, [
      { key: "zone" },
      { key: "category" },
      { key: "status" }
    ], "No complaints submitted yet.");

  } catch (error) {
    console.error("Dashboard update failed:", error);
    if (connection) {
      connection.textContent = "● Connection error";
      connection.classList.add("disconnected");
      connection.classList.remove("connected");
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const button = $("refreshBtn");
  if (button) button.addEventListener("click", refreshDashboard);

  refreshDashboard();
  window.setInterval(refreshDashboard, 5000);
});
