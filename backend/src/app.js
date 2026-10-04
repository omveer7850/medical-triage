const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const connectDB = require('./config/db');
const apiRoutes = require('./routes/api');

// Load environment variables
dotenv.config();

// Connect to MongoDB
connectDB();

const app = express();

// Private Network Access (PNA) & CORS Middleware
// Allows public HTTPS origins (e.g. Vercel) to interact with local loopback backend
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  res.setHeader('Access-Control-Allow-Private-Network', 'true');
  
  if (req.method === 'OPTIONS') {
    return res.sendStatus(204);
  }
  next();
});

app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['*']
}));

app.use(express.json({ limit: '15mb' }));
app.use(express.urlencoded({ extended: true, limit: '15mb' }));

// Base Route
app.get('/', (req, res) => {
  res.json({
    status: 'online',
    service: 'Medical Triage Backend Server',
    time: new Date()
  });
});

// Register routes
app.use('/api', apiRoutes);

// Error Handling Middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error', message: err.message });
});

module.exports = app;
