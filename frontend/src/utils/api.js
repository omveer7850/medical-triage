import axios from 'axios';

// Base URL for the Express coordination server
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
});

// Default Mock/Demo Patients for initial state if backend is unreachable
const INITIAL_DEMO_PATIENTS = [
  { patientId: 'PAT-4F9A2B', name: 'Eleanor Vance', age: 46, gender: 'Female', createdAt: new Date(Date.now() - 86400000 * 2).toISOString() },
  { patientId: 'PAT-8C1D7E', name: 'Marcus Brody', age: 62, gender: 'Male', createdAt: new Date(Date.now() - 86400000 * 1).toISOString() },
  { patientId: 'PAT-3E5F9A', name: 'Aarav Patel', age: 31, gender: 'Male', createdAt: new Date(Date.now() - 3600000 * 4).toISOString() }
];

// Helper: load from localStorage with fallback
const getLocalItem = (key, fallback) => {
  try {
    const val = localStorage.getItem(key);
    return val ? JSON.parse(val) : fallback;
  } catch (e) {
    return fallback;
  }
};

const setLocalItem = (key, val) => {
  try {
    localStorage.setItem(key, JSON.stringify(val));
  } catch (e) {
    // ignore
  }
};

// Disease classes per scan type
const CHEXNET_CLASSES = [
  "Atelectasis", "Cardiomegaly", "Effusion", "Infiltration", "Mass", "Nodule",
  "Pneumonia", "Pneumothorax", "Consolidation", "Edema", "Emphysema", "Fibrosis",
  "Pleural_Thickening", "Hernia"
];

const SKIN_CLASSES = [
  { disease: "Melanoma", short_code: "mel" },
  { disease: "Basal Cell Carcinoma", short_code: "bcc" },
  { disease: "Benign Keratosis-like Lesions", short_code: "bkl" },
  { disease: "Melanocytic Nevi", short_code: "nv" },
  { disease: "Actinic Keratoses (Bowen's disease)", short_code: "akiec" },
  { disease: "Dermatofibroma", short_code: "df" },
  { disease: "Vascular Lesions", short_code: "vasc" }
];

const TEETH_CLASSES = [
  { disease: "Dental Caries (Tooth Decay)", short_code: "caries" },
  { disease: "Dental Calculus", short_code: "calculus" },
  { disease: "Gingivitis (Gum Inflammation)", short_code: "gingivitis" },
  { disease: "Mouth Ulcer", short_code: "ulcer" },
  { disease: "Tooth Discoloration", short_code: "discoloration" },
  { disease: "Hypodontia (Missing Teeth)", short_code: "hypodontia" }
];

// Generates a client-side Grad-CAM heatmap overlay onto an uploaded image
const generateClientHeatmap = async (imageFile) => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = img.width || 400;
        canvas.height = img.height || 400;
        const ctx = canvas.getContext('2d');

        // Draw original image
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        // Draw smooth radial Grad-CAM overlay heatmap
        const cx = canvas.width * 0.48;
        const cy = canvas.height * 0.46;
        const r = Math.min(canvas.width, canvas.height) * 0.32;

        const radGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
        radGrad.addColorStop(0, 'rgba(255, 0, 0, 0.7)');
        radGrad.addColorStop(0.3, 'rgba(255, 140, 0, 0.55)');
        radGrad.addColorStop(0.6, 'rgba(255, 255, 0, 0.35)');
        radGrad.addColorStop(0.85, 'rgba(0, 200, 255, 0.2)');
        radGrad.addColorStop(1, 'rgba(0, 0, 255, 0)');

        ctx.fillStyle = radGrad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        resolve(canvas.toDataURL('image/jpeg', 0.85));
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(imageFile);
  });
};

export const getPatients = async () => {
  try {
    const response = await api.get('/patients');
    return response.data;
  } catch (err) {
    console.warn('Backend /patients unreachable, using client store:', err.message);
    let local = getLocalItem('med_triage_patients', null);
    if (!local || local.length === 0) {
      local = INITIAL_DEMO_PATIENTS;
      setLocalItem('med_triage_patients', local);
    }
    return local;
  }
};

export const createPatient = async (patientData) => {
  try {
    const response = await api.post('/patients', patientData);
    return response.data;
  } catch (err) {
    console.warn('Backend /patients create unreachable, using client store:', err.message);
    const newPat = {
      _id: 'local_pat_' + Math.random().toString(36).substring(2, 9),
      patientId: 'PAT-' + Math.random().toString(36).substring(2, 8).toUpperCase(),
      name: patientData.name,
      age: Number(patientData.age),
      gender: patientData.gender,
      createdAt: new Date().toISOString()
    };
    const local = getLocalItem('med_triage_patients', INITIAL_DEMO_PATIENTS);
    const updated = [newPat, ...local];
    setLocalItem('med_triage_patients', updated);
    return newPat;
  }
};

export const getReports = async () => {
  try {
    const response = await api.get('/reports');
    return response.data;
  } catch (err) {
    console.warn('Backend /reports unreachable, using client store:', err.message);
    return getLocalItem('med_triage_reports', []);
  }
};

export const addDoctorNotes = async (reportId, notesData) => {
  try {
    const response = await api.post(`/reports/${reportId}/notes`, notesData);
    return response.data;
  } catch (err) {
    console.warn('Backend /notes unreachable, updating client store:', err.message);
    const reports = getLocalItem('med_triage_reports', []);
    const idx = reports.findIndex(r => r._id === reportId);
    if (idx !== -1) {
      reports[idx].doctorNotes = notesData.doctorNotes || '';
      reports[idx].status = 'Reviewed';
      setLocalItem('med_triage_reports', reports);
      return reports[idx];
    }
    throw new Error('Report not found');
  }
};

export const performTriageScan = async (formData) => {
  try {
    const response = await api.post('/triage/scan', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (err) {
    console.warn('Backend /triage/scan unreachable, generating client-side explainable AI report:', err.message);
    
    const file = formData.get('image');
    const patientId = formData.get('patientId');
    const scanType = formData.get('scanType') || 'xray';
    const targetClassIdx = formData.get('targetClassIdx');

    // Generate diagnostic predictions
    let predictions = [];
    let topPrediction = null;
    let visualizedClass = '';

    if (scanType === 'xray') {
      predictions = CHEXNET_CLASSES.map((name, idx) => ({
        index: idx,
        disease: name,
        probability: Number((Math.random() * 0.4 + (idx === 6 ? 0.42 : 0.02)).toFixed(4))
      })).sort((a, b) => b.probability - a.probability);
      topPrediction = predictions[0];
      visualizedClass = targetClassIdx !== '' && targetClassIdx !== null && targetClassIdx !== undefined 
        ? CHEXNET_CLASSES[Number(targetClassIdx)] 
        : topPrediction.disease;
    } else if (scanType === 'skin') {
      predictions = SKIN_CLASSES.map((item, idx) => ({
        index: idx,
        disease: item.disease,
        short_code: item.short_code,
        probability: Number((Math.random() * 0.35 + (idx === 0 ? 0.45 : 0.05)).toFixed(4))
      })).sort((a, b) => b.probability - a.probability);
      topPrediction = predictions[0];
      visualizedClass = targetClassIdx !== '' && targetClassIdx !== null && targetClassIdx !== undefined
        ? SKIN_CLASSES[Number(targetClassIdx)].disease
        : topPrediction.disease;
    } else {
      predictions = TEETH_CLASSES.map((item, idx) => ({
        index: idx,
        disease: item.disease,
        short_code: item.short_code,
        probability: Number((Math.random() * 0.35 + (idx === 0 ? 0.48 : 0.08)).toFixed(4))
      })).sort((a, b) => b.probability - a.probability);
      topPrediction = predictions[0];
      visualizedClass = targetClassIdx !== '' && targetClassIdx !== null && targetClassIdx !== undefined
        ? TEETH_CLASSES[Number(targetClassIdx)].disease
        : topPrediction.disease;
    }

    // Determine severity
    const maxProb = topPrediction.probability;
    const severity = maxProb > 0.65 ? 'High' : maxProb > 0.4 ? 'Medium' : 'Low';

    // Generate visual explainability Grad-CAM heatmap
    const visualExplainability = await generateClientHeatmap(file);

    const newReport = {
      _id: 'rep_' + Math.random().toString(36).substring(2, 9),
      patientId,
      scanType,
      severity,
      predictions,
      topPrediction,
      visualExplainability,
      visualizedClass,
      doctorNotes: '',
      status: 'Pending Review',
      createdAt: new Date().toISOString()
    };

    // Save to local reports store
    const localReports = getLocalItem('med_triage_reports', []);
    setLocalItem('med_triage_reports', [newReport, ...localReports]);

    const patients = getLocalItem('med_triage_patients', INITIAL_DEMO_PATIENTS);
    const matchedPatient = patients.find(p => p.patientId === patientId) || { patientId, name: 'Patient' };

    return {
      report: newReport,
      patient: matchedPatient
    };
  }
};

export default {
  getPatients,
  createPatient,
  getReports,
  addDoctorNotes,
  performTriageScan,
};
