document.addEventListener("DOMContentLoaded", function () {
  const customerContainer = document.getElementById("customerContainer");
  const generateBtn = document.getElementById("generateBtn");
  const customerCountInput = document.getElementById("customerCount");
  const responseContainer = document.getElementById("responseContainer");

  // Simulated TCP connection through browser APIs
  class TCPSimulator {
    constructor() {
      this.ws = new WebSocket("ws://localhost:8080");
      this.queue = [];
    }

    connect() {
      return new Promise((resolve, reject) => {
        this.ws.onopen = () => resolve();
        this.ws.onerror = (err) => reject(err);
      });
    }

    send(data) {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify(data));
      } else {
        this.queue.push(data);
      }
    }

    onMessage(callback) {
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          callback(data);
        } catch (e) {
          console.error("Invalid JSON:", event.data);
        }
      };
    }
  }

  const tcp = new TCPSimulator();

  tcp
    .connect()
    .then(() => {
      console.log("Connected to TCP server via WebSocket proxy");
      // Process queued messages
      tcp.queue.forEach((msg) => tcp.send(msg));
      tcp.queue = [];
    })
    .catch((err) => {
      console.error("Connection error:", err);
    });

  tcp.onMessage((data) => {
    displayResponse(data);
  });

  function displayResponse(data) {
    const responseElement = document.createElement("div");
    responseElement.className = "response-message";
    responseElement.innerHTML = `
            <p><strong>${data.name}:</strong> ${data.message}</p>
            <small>${new Date().toLocaleTimeString()}</small>
        `;
    responseContainer.prepend(responseElement);
  }

  generateBtn.addEventListener("click", function () {
    const count = parseInt(customerCountInput.value) || 1;
    customerContainer.innerHTML = "";

    if (count > 20) {
      alert("Maximum of 20 customers allowed");
      return;
    }

    for (let i = 1; i <= count; i++) {
      const customerData = {
        id: i,
        name: `Customer ${i}`,
        message: `Initialized connection`,
      };

      tcp.send(customerData);
      const card = createCustomerCard(customerData);
      customerContainer.appendChild(card);
    }
  });

  function createCustomerCard(customer) {
    const card = document.createElement("div");
    card.className = "customer-card";
    card.innerHTML = `
            <div class="customer-header">
                <div class="customer-avatar">${customer.id}</div>
                <div class="customer-info">
                    <h3>${customer.name}</h3>
                    <p>Status: Connected</p>
                </div>
            </div>
            <div class="customer-message">
                <textarea id="message-${customer.id}" placeholder="Type message"></textarea>
                <button class="send-btn" data-id="${customer.id}">Send</button>
            </div>
        `;

    card.querySelector(".send-btn").addEventListener("click", function () {
      const customerId = this.getAttribute("data-id");
      const message = document.getElementById(`message-${customerId}`).value;

      if (message.trim() === "") {
        alert("Please enter a message");
        return;
      }

      tcp.send({
        id: customerId,
        name: `Customer ${customerId}`,
        message: message,
        family: "Kondratev",
      });
    });

    return card;
  }
});
