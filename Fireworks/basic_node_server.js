const express = require('express');
const path = require('path');
const mqtt = require('mqtt');
const WebSocket = require('ws');

const app = express();
const port = 3000;

// Serve static files
app.use(express.static(path.join(__dirname, '.')));

// Create a WebSocket server
const wss = new WebSocket.Server({ server: app.listen(port) });

// MQTT client
const mqttClient = mqtt.connect('mqtt://192.168.222.150:1883');

mqttClient.on('connect', () => {
  mqttClient.subscribe('/fireworks');
});

mqttClient.on('message', (topic, message) => {
    // console.log(`Received message on topic ${topic}:`, message.toString());
    if (topic === '/fireworks') {
      try {
        const data = JSON.parse(message.toString().trim());
        handleFireworksData(data);
      } catch (e) {
        console.error('Error parsing MQTT message:', e);
      }
    }
  });
  

function handleFireworksData(data) {
  if (data.special === 1) {
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send('trigger-special-firework-1');
      }
    });
  }
  else if (data.special === 2){
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
          client.send('trigger-special-firework-2');
        }
      });

  }
  else if (data.special === 3){
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
          client.send('trigger-special-firework-3');
        }
      });

  }
  else {
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
          client.send('trigger-firework');
        }
      });

  }
  // Add more conditions for other 'special' values if needed
}

console.log(`Server is running at http://localhost:${port}`);
