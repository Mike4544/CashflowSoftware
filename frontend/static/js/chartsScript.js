var charts = [];

async function addChart() {
  const chartType = document.getElementById("chartType").value;

  const chartContainer = document.getElementById("chart-container");
  const chartWrapper = document.createElement("div");
  chartWrapper.className = "col-md-12 chart-wrapper";

  const canvas = document.createElement("canvas");
  const chartId = `chart-${charts.length}`;
  canvas.id = chartId;
  // canvas.width = 10;
  // canvas.height = 10;

  chartWrapper.appendChild(canvas);
  chartContainer.appendChild(chartWrapper);

  // Inițializează noul grafic
  const ctx = canvas.getContext("2d");
  const currentChart = new Chart(ctx, {
    type: chartType,
    data: {
      labels: [],
      datasets: [
        {
          label: `${chartType} Chart`,
          data: [],
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: { beginAtZero: true },
        y: { beginAtZero: true },
      },
    },
  });

  charts.push({ id: chartId, chart: currentChart });

  //  Send the chart to the server
  const response = await fetch("/api/charts/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: chartId,
      type: chartType,
      data: {
        labels: [],
        datasets: [
          {
            label: `${chartType} Chart`,
            data: [],
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          x: { beginAtZero: true },
          y: { beginAtZero: true },
        },
      },
    }),
  });

  if (response.ok) {
    console.log("Success!");
  } else {
    console.log("Error!");
  }

  setupTable(currentChart);
}

function loadChart(chart) {
  const chartType = chart.type;

  const chartContainer = document.getElementById("chart-container");
  const chartWrapper = document.createElement("div");
  chartWrapper.className = "col-md-12 chart-wrapper";

  const canvas = document.createElement("canvas");
  const chartId = chart.id;
  canvas.id = chartId;
  // canvas.width = 10;
  // canvas.height = 10;

  chartWrapper.appendChild(canvas);
  chartContainer.appendChild(chartWrapper);

  console.log(chart.data);

  const ctx = canvas.getContext("2d");
  const currentChart = new Chart(ctx, {
    type: chartType,
    data: chart.data,
    options: {
      responsive: true,
      scales: {
        x: { beginAtZero: true },
        y: { beginAtZero: true },
      },
    },
  });

  console.log("done");

  charts.push({ id: chartId, chart: currentChart });

  setupTable(currentChart);
}

function setupTable(chart) {
  const chartContainer = document.getElementById("chart-container");
  const chartId = chart.canvas.id;
  const tableWrapper = document.createElement("div");
  tableWrapper.className = "col-md-12 data-table";

  const table = document.createElement("table");
  table.className = "table";
  const tableBody = document.createElement("tbody");
  tableBody.id = `table-body-${chartId}`;
  table.appendChild(tableBody);

  const buttonRow = document.createElement("div");
  buttonRow.className = "row";
  buttonRow.innerHTML = `
      <div class="col-md-4">
        <button onclick="addData('${chartId}')" class="btn btn-success m-1">Adaugă Date</button>
      </div>
      <div class="col-md-4">
        <button onclick="deleteChart('${chartId}')" class="btn btn-danger m-1">Șterge Grafic</button>
      </div>
    `;

  tableWrapper.appendChild(table);
  tableWrapper.appendChild(buttonRow);
  chartContainer.appendChild(tableWrapper);

  // For existing data in the chart, load the rows
  chart.data.labels.forEach((label, index) => {
    addRow(chart, label, chart.data.datasets[0].data[index]);
});

}

function addData(chartId) {
  const chart = findChart(chartId);
  addRow(chart);
}

function updateData(chartId) {
  const chart = findChart(chartId);
  const tableRows = document.querySelectorAll(`#table-body-${chartId} tr`);
  tableRows.forEach((row) => updateChart(row.querySelector("button"), chart));
}

function deleteData(chartId) {
  const chart = findChart(chartId);
  const tableRows = document.querySelectorAll(`#table-body-${chartId} tr`);
  tableRows.forEach((row) => deleteRow(row.querySelector("button"), chart));
}

function addRow(chart, label = "", value = "") {
  const tableBody = document.getElementById(`table-body-${chart.canvas.id}`);
  const newRow = document.createElement("tr");
  newRow.innerHTML = `
      <td><input type="text" class="form-control" value="${label}"></td>
      <td><input type="number" class="form-control" value="${value}"></td>
      <td>
        <button onclick="updateChart(this, '${chart.canvas.id}')" class = "btn btn-warning m-1">Modifica Categorie</button>
        <button onclick="deleteRow(this, '${chart.canvas.id}')" class="btn btn-danger m-1">Sterge Categorie</button>
      </td>
    `;

  tableBody.appendChild(newRow);
}

async function updateChart(button, chartId) {
  const tableRow = button.parentNode.parentNode;
  const labelInput = tableRow.querySelector('input[type="text"]');
  const valueInput = tableRow.querySelector('input[type="number"]');
  const chart = findChart(chartId);

  const chartType = chart.config.type;

  if (!labelInput.value || isNaN(valueInput.value)) {
    alert("Introduceți o etichetă și o valoare valide.");
    return;
  }

  const index = chart.data.labels.indexOf(labelInput.value);
  if (index !== -1) {
    // Update existing label
    chart.data.datasets[0].data[index] = parseFloat(valueInput.value);
  } else {
    // Add new label
    chart.data.labels.push(labelInput.value);
    chart.data.datasets[0].data.push(parseFloat(valueInput.value));
  }

  // Send the chart to the server
  const response = await fetch("/api/charts/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: chartId,
      type: chartType,
      data: chart.data,
      options: chart.options,
    }),
  });

  if (response.ok) {
    console.log("Success!");
  } else {
    console.log("Error!");
  }

  chart.update();
}

async function deleteRow(button, chartId) {
  const tableRow = button.parentNode.parentNode;
  const chart = findChart(chartId);
  const labelInput = tableRow.querySelector('input[type="text"]');
  const index = chart.data.labels.indexOf(labelInput.value);

  if (index !== -1) {
    // Remove label and value from chartData
    chart.data.labels.splice(index, 1);
    chart.data.datasets[0].data.splice(index, 1);

    // Update the chart
    chart.update();
  }

  // Send the chart to the server
  const response = await fetch("/api/charts/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: chartId,
      type: chart.config.type,
      data: chart.data,
      options: chart.options,
    }),
  });

  if (response.ok) {
    console.log("Success!");
  } else {
    console.log("Error!");
  }

  // Remove the table row
  tableRow.remove();
}

function findChart(chartId) {
  // Găsește și returnează obiectul Chart corespunzător
  return charts.find((chart) => chart.id === chartId).chart;
}

async function deleteChart(chartId) {
  // Găsește și elimină graficul din array-ul charts
  const chartIndex = charts.findIndex((chart) => chart.id === chartId);
  if (chartIndex !== -1) {
    charts.splice(chartIndex, 1);
  }

  // Elimină div-ul care conține graficul și tabelul
  const chartWrapper = document.getElementById(chartId).parentNode;
  chartWrapper.remove();

  // Elimină și tabelul asociat
  const tableBody = document.getElementById(`table-body-${chartId}`);
  if (tableBody) {
    tableBody.parentNode.parentNode.remove();
  }

  //  Send the chart to the server
  const response = await fetch("/api/charts/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: chartId,
    }),
  });

  if (response.ok) {
    console.log("Success!");
  } else {
    console.log("Error!");
  }
}
