const WebSocket = require("ws");

const server = new WebSocket.Server({ port: process.env.PORT || 3000 });

let clients = [];

server.on("connection", (ws) => {
  clients.push(ws);

  ws.on("message", (msg) => {
    // Nachricht an alle Clients weiterleiten
    for (const client of clients) {
      if (client.readyState === WebSocket.OPEN) {
        client.send(msg);
      }
    }
  });

  ws.on("close", () => {
    clients = clients.filter(c => c !== ws);
  });
});

console.log("Cloud-Server läuft!");
