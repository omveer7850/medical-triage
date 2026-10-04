const express = require('express');
const router = express.Router();
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const mongoose = require('mongoose');
const Patient = require('../models/Patient');
const Report = require('../models/Report');

// Setup multer for memory storage
const storage = multer.memoryStorage();
const upload = multer({ 
  storage: storage,
  limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
});

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';

// Global In-Memory Fallback Stores (used if MongoDB is offline)
let inMemoryPatients = [];
let inMemoryReports = [];

// Helper: Generates a random alphanumeric patient ID
const generatePatientId = () => {
  return 'PAT-' + Math.random().toString(36).substring(2, 9).toUpperCase();
};

/**
 * @route   GET /api/patients
 * @desc    Get all patients list
 */
router.get('/patients', async (req, res) => {
  try {
    if (mongoose.connection.readyState === 1) {
      const patients = await Patient.find().sort({ createdAt: -1 });
      res.json(patients);
    } else {
      console.log('Using in-memory patient store fallback');
      const sorted = [...inMemoryPatients].sort((a, b) => b.createdAt - a.createdAt);
      res.json(sorted);
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * @route   POST /api/patients
 * @desc    Create / register a new patient
 */
router.post('/patients', async (req, res) => {
  const { name, age, gender } = req.body;
  if (!name || !age || !gender) {
    return res.status(400).json({ error: 'Name, age, and gender are required' });
  }
  
  try {
    const patientId = generatePatientId();
    if (mongoose.connection.readyState === 1) {
      const newPatient = new Patient({ patientId, name, age, gender });
      await newPatient.save();
      res.status(201).json(newPatient);
    } else {
      console.log('Saving to in-memory patient store fallback');
      const newPatient = {
        _id: 'mem_pat_' + Math.random().toString(36).substring(2, 9),
        patientId,
        name,
        age: Number(age),
        gender,
        createdAt: new Date()
      };
      inMemoryPatients.push(newPatient);
      res.status(201).json(newPatient);
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * @route   GET /api/reports
 * @desc    Get all reports / triage queue
 */
router.get('/reports', async (req, res) => {
  try {
    if (mongoose.connection.readyState === 1) {
      const reports = await Report.find().sort({ createdAt: -1 });
      res.json(reports);
    } else {
      console.log('Using in-memory report store fallback');
      const sorted = [...inMemoryReports].sort((a, b) => b.createdAt - a.createdAt);
      res.json(sorted);
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * @route   POST /api/reports/:id/notes
 * @desc    Update doctor notes and set status to "Reviewed"
 */
router.post('/reports/:id/notes', async (req, res) => {
  const { doctorNotes } = req.body;
  try {
    if (mongoose.connection.readyState === 1) {
      const report = await Report.findById(req.params.id);
      if (!report) {
        return res.status(404).json({ error: 'Report not found' });
      }
      
      report.doctorNotes = doctorNotes || '';
      report.status = 'Reviewed';
      await report.save();
      
      res.json(report);
    } else {
      console.log('Updating in-memory report notes fallback');
      const report = inMemoryReports.find(r => r._id === req.params.id);
      if (!report) {
        return res.status(404).json({ error: 'Report not found' });
      }
      report.doctorNotes = doctorNotes || '';
      report.status = 'Reviewed';
      res.json(report);
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * @route   POST /api/triage/scan
 * @desc    Upload image, query ML microservice, save diagnostic report in DB
 */
router.post('/triage/scan', upload.single('image'), async (req, res) => {
  const { patientId, scanType, targetClassIdx } = req.body;
  
  if (!req.file) {
    return res.status(400).json({ error: 'No image file uploaded' });
  }
  if (!patientId || !scanType) {
    return res.status(400).json({ error: 'patientId and scanType (xray, skin, or teeth) are required' });
  }
  if (!['xray', 'skin', 'teeth'].includes(scanType)) {
    return res.status(400).json({ error: 'Invalid scanType. Must be xray, skin, or teeth' });
  }
  
  try {
    // 1. Check if patient exists
    let patientExists;
    if (mongoose.connection.readyState === 1) {
      patientExists = await Patient.findOne({ patientId });
    } else {
      patientExists = inMemoryPatients.find(p => p.patientId === patientId);
    }
    
    if (!patientExists) {
      return res.status(404).json({ error: `Patient ID ${patientId} not found` });
    }
    
    // 2. Prepare multipart data to forward to FastAPI
    const form = new FormData();
    form.append('file', req.file.buffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype,
    });
    
    // Construct target URL for FastAPI
    let mlEndpoint = `${ML_SERVICE_URL}/api/predict/${scanType}`;
    if (targetClassIdx !== undefined && targetClassIdx !== '') {
      mlEndpoint += `?target_class_idx=${targetClassIdx}`;
    }
    
    console.log(`Forwarding scan request to ML Service: ${mlEndpoint}`);
    
    // 3. Make the API call to FastAPI
    const mlResponse = await axios.post(mlEndpoint, form, {
      headers: {
        ...form.getHeaders(),
      },
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
    });
    
    const mlResult = mlResponse.data;
    
    // 4. Save results to the MongoDB database / or Memory Fallback
    const reportData = {
      patientId,
      scanType,
      severity: mlResult.severity,
      predictions: mlResult.predictions,
      topPrediction: {
        disease: mlResult.top_prediction.disease,
        probability: mlResult.top_prediction.probability,
      },
      visualExplainability: mlResult.visual_explainability,
      visualizedClass: mlResult.visualized_class,
      status: 'Pending Review',
      createdAt: new Date()
    };
    
    let savedReport;
    if (mongoose.connection.readyState === 1) {
      const newReport = new Report(reportData);
      savedReport = await newReport.save();
    } else {
      console.log('Saving scan report to in-memory store fallback');
      savedReport = {
        _id: 'mem_rep_' + Math.random().toString(36).substring(2, 9),
        ...reportData
      };
      inMemoryReports.push(savedReport);
    }
    
    res.status(201).json({
      report: savedReport,
      patient: patientExists
    });
    
  } catch (error) {
    console.error('Triage scanning process failed:', error.message);
    if (error.response) {
      res.status(502).json({ error: `ML Service Error: ${error.response.data.detail || error.response.statusText}` });
    } else {
      res.status(500).json({ error: `Scans triage failed: ${error.message}` });
    }
  }
});

module.exports = router;
