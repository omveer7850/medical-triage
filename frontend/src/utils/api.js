import axios from 'axios';

// Base URL for the Express coordination server
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getPatients = async () => {
  const response = await api.get('/patients');
  return response.data;
};

export const createPatient = async (patientData) => {
  const response = await api.post('/patients', patientData);
  return response.data;
};

export const getReports = async () => {
  const response = await api.get('/reports');
  return response.data;
};

export const addDoctorNotes = async (reportId, notesData) => {
  const response = await api.post(`/reports/${reportId}/notes`, notesData);
  return response.data;
};

export const performTriageScan = async (formData) => {
  const response = await api.post('/triage/scan', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export default {
  getPatients,
  createPatient,
  getReports,
  addDoctorNotes,
  performTriageScan,
};
