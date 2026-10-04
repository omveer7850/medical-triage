const mongoose = require('mongoose');

const ReportSchema = new mongoose.Schema({
  patientId: {
    type: String,
    required: true,
  },
  scanType: {
    type: String,
    required: true,
    enum: ['xray', 'skin', 'teeth'],
  },
  severity: {
    type: String,
    required: true,
    enum: ['Low', 'Medium', 'High'],
  },
  predictions: [
    {
      disease: String,
      probability: Number,
      index: Number,
      short_code: String
    }
  ],
  topPrediction: {
    disease: String,
    probability: Number
  },
  visualExplainability: {
    type: String, // Base64 data URI of the Grad-CAM image overlay
  },
  visualizedClass: {
    type: String,
  },
  doctorNotes: {
    type: String,
    default: '',
  },
  status: {
    type: String,
    default: 'Pending Review',
    enum: ['Pending Review', 'Reviewed'],
  },
  createdAt: {
    type: Date,
    default: Date.now,
  }
});

module.exports = mongoose.model('Report', ReportSchema);
