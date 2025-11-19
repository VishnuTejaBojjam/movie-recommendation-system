const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();
const API_SERVICE_URL = process.env.BACKEND_URL || 'http://127.0.0.1:5000';

// Proxy API requests to Python Flask backend
app.use('/movies', createProxyMiddleware({ target: API_SERVICE_URL, changeOrigin: true }));
app.use('/recommend', createProxyMiddleware({ target: API_SERVICE_URL, changeOrigin: true }));

// Serve static frontend files
app.use(express.static(path.join(__dirname, 'frontend')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Node server listening on ${port}. Proxying API to ${API_SERVICE_URL}`);
});
