const ws = new WebSocket("ws://localhost:8080/stream");

const tableBody = document.querySelector("#client-table tbody");
const stats = document.getElementById("stats");

let served = 0;
let income = 0;

ws.onmessage = function (event) {
  const client = JSON.parse(event.data);

  const row = document.createElement("tr");
  row.className = client.Result === "Саванна" ? "savanna" : "hotel";

  const budgetCell = document.createElement("td");
  budgetCell.textContent = `${client.Budget} быров`;

  const resultCell = document.createElement("td");
  resultCell.textContent = client.Result;

  const priceCell = document.createElement("td");
  priceCell.textContent = client.Price > 0 ? `${client.Price} быров` : "-";

  row.appendChild(budgetCell);
  row.appendChild(resultCell);
  row.appendChild(priceCell);

  tableBody.appendChild(row);

  if (client.Result !== "Саванна") {
    served++;
    income += client.Price;
  }

  stats.textContent = `Клиенты: ${tableBody.children.length} | Заселено: ${served} | Доход: ${income}`;
};
