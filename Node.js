const WebSocket = require("ws");

// Adresse deines bestehenden TurboWarp-Cloud-Servers
const TARGET = "wss://DEIN-SERVER.onrender.com"; 

// Adapter-Server (nimmt Packager-Cloud-Protokoll an)
const adapter = new WebSocket.Server({
  port: process.env.PORT || 3000
});

console.log("Adapter läuft auf Port", process.env.PORT || 3000);

adapter.on("connection", client => {
  console.log("Client verbunden");

  // Verbindung zum echten TurboWarp-Cloud-Server
  const target = new WebSocket(TARGET);

  target.on("open", () => {
    console.log("Verbunden mit echtem Cloud-Server");
  });

  target.on("message", msg => {
    // Der echte Server sendet JSON → wir wandeln es in Text um
    try {
      const lines = msg.toString().split("\n");
      for (const line of lines) {
        const data = JSON.parse(line);
        if (data.method === "set") {
          client.send(`set ${data.name} ${data.value}`);
        }
      }
    } catch (e) {
      console.log("Fehler beim Parsen:", e);
    }
  });

  client.on("message", msg => {
    const text = msg.toString().trim();
    const parts = text.split(" ");

    // Packager sendet: set name value
    if (parts[0] === "set") {
      const name = parts[1];
      const value = parts.slice(2).join(" ");

      const json = JSON.stringify({
        method: "set",
        name: name,
        value: value
      });

      target.send(json);
    }
  });

  client.on("close", () => {
    console.log("Client getrennt");
    target.close();
  });
});
