import React, { useState, useEffect } from 'react';
import { getPatients, performTriageScan } from '../utils/api';
import { Upload, FileText, CheckCircle, ShieldAlert, Image as ImageIcon } from 'lucide-react';

const SKIN_CLASSES = [
  "Actinic Keratoses (Bowen's disease)",
  "Basal Cell Carcinoma",
  "Benign Keratosis-like Lesions",
  "Dermatofibroma",
  "Melanoma",
  "Melanocytic Nevi",
  "Vascular Lesions"
];

export default function SkinTriage({ onScanComplete }) {
  const [patients, setPatients] = useState([]);
  const [selectedPatientId, setSelectedPatientId] = useState('');
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [targetClassIdx, setTargetClassIdx] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const data = await getPatients();
        setPatients(data || []);
        if (data && data.length > 0) {
          setSelectedPatientId(data[0].patientId);
        }
      } catch (err) {
        console.error("Failed to load patients", err);
      }
    };
    fetchPatients();
  }, []);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreviewUrl(URL.createObjectURL(selectedFile));
      setResult(null);
      setError('');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      setPreviewUrl(URL.createObjectURL(droppedFile));
      setResult(null);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !selectedPatientId) {
      setError("Please select both a patient and an image file.");
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      const formData = new FormData();
      formData.append('image', file);
      formData.append('patientId', selectedPatientId);
      formData.append('scanType', 'skin');
      if (targetClassIdx !== '') {
        formData.append('targetClassIdx', targetClassIdx);
      }

      const response = await performTriageScan(formData);
      setResult(response.report);
      if (onScanComplete) {
        onScanComplete();
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || "Triage scan submission failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <h1 className="page-title">Dermatological Image Analysis & Triage</h1>

      <div className="triage-grid">
        {/* Left Card: Upload Form */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '20px' }}>Upload Dermatoscopic Image</h3>
          <form onSubmit={handleSubmit}>
            
            {/* Patient Select */}
            <div className="form-group">
              <label>Target Patient Profile</label>
              {patients.length === 0 ? (
                <div style={{ fontSize: '13px', color: 'var(--color-medium)' }}>
                  No patients registered. Please go to the Triage Board first to register a patient.
                </div>
              ) : (
                <select 
                  value={selectedPatientId} 
                  onChange={(e) => setSelectedPatientId(e.target.value)} 
                  className="form-control"
                >
                  {patients.map(p => (
                    <option key={p.patientId} value={p.patientId}>
                      {p.name} ({p.patientId}, Age {p.age})
                    </option>
                  ))}
                </select>
              )}
            </div>

            {/* Target Class (Grad-CAM) */}
            <div className="form-group">
              <label>Focus Lesion Type for Grad-CAM (Optional)</label>
              <select 
                value={targetClassIdx} 
                onChange={(e) => setTargetClassIdx(e.target.value)} 
                className="form-control"
              >
                <option value="">Auto (Visualize Highest Probability Lesion)</option>
                {SKIN_CLASSES.map((name, idx) => (
                  <option key={idx} value={idx}>{name}</option>
                ))}
              </select>
            </div>

            {/* File Drag & Drop Box */}
            <div className="form-group" style={{ marginTop: '16px' }}>
              <label>Dermatoscopic Image File</label>
              <div 
                className="upload-container" 
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => document.getElementById('skin-file-input').click()}
              >
                <input 
                  type="file" 
                  id="skin-file-input" 
                  accept="image/*" 
                  onChange={handleFileChange} 
                  style={{ display: 'none' }} 
                />
                
                {previewUrl ? (
                  <img src={previewUrl} alt="Preview" style={{ maxHeight: '180px', borderRadius: '8px', objectFit: 'contain' }} />
                ) : (
                  <>
                    <Upload size={32} className="upload-icon" />
                    <div>
                      <p style={{ fontWeight: '500' }}>Drag & Drop skin scan here</p>
                      <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '4px' }}>Supports PNG, JPG, JPEG (up to 10MB)</p>
                    </div>
                  </>
                )}
              </div>
            </div>

            {error && (
              <div style={{ color: 'var(--color-high)', fontSize: '13px', margin: '12px 0' }}>
                {error}
              </div>
            )}

            <button 
              type="submit" 
              className="btn-glow" 
              style={{ width: '100%', marginTop: '16px', background: 'linear-gradient(135deg, var(--color-accent-purple) 0%, var(--color-accent-pink) 100%)', boxShadow: '0 4px 14px 0 rgba(185, 39, 252, 0.3)' }}
              disabled={loading || !file || patients.length === 0}
            >
              {loading ? "Running Deep Learning Inference..." : "Submit for Triage Scans"}
            </button>
          </form>
        </div>

        {/* Right Card: Result Display */}
        <div>
          {result ? (
            <div className="glass-card" style={{ border: `1px solid ${result.severity === 'High' ? 'rgba(239, 68, 68, 0.3)' : result.severity === 'Medium' ? 'rgba(245, 158, 11, 0.3)' : 'rgba(255, 255, 255, 0.08)'}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <h3>Inference Results</h3>
                <span className={`badge ${result.severity.toLowerCase()}`}>
                  {result.severity} Risk
                </span>
              </div>

              {/* Image Split */}
              <div className="image-display-grid">
                <div className="image-box">
                  {previewUrl && <img src={previewUrl} alt="Original input" />}
                  <div className="image-label">Original Input</div>
                </div>
                <div className="image-box">
                  {result.visualExplainability ? (
                    <img src={result.visualExplainability} alt="Grad-CAM heatmap" />
                  ) : (
                    <div style={{ padding: '20px', textAlign: 'center', color: 'var(--color-text-muted)', fontSize: '13px' }}>Generating heatmap...</div>
                  )}
                  <div className="image-label">Grad-CAM: {result.visualizedClass}</div>
                </div>
              </div>

              {/* Predictions Summary */}
              <div style={{ marginTop: '24px' }}>
                <h4 style={{ marginBottom: '12px' }}>Skin Lesion Classification Breakdown</h4>
                <div className="prediction-list">
                  {result.predictions
                    .slice()
                    .sort((a, b) => b.probability - a.probability)
                    .map((pred, i) => (
                      <div key={i} className="prediction-row">
                        <div className="prediction-label">
                          <span>{pred.disease} ({pred.short_code})</span>
                          <span style={{ fontWeight: '600' }}>{(pred.probability * 100).toFixed(2)}%</span>
                        </div>
                        <div className="prediction-bar-bg">
                          <div className="prediction-bar-fill accent" style={{ width: `${pred.probability * 100}%` }} />
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="glass-card" style={{ textAlign: 'center', padding: '120px 20px', color: 'var(--color-text-muted)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '12px' }}>
              <ImageIcon size={40} strokeWidth={1.5} color="var(--color-text-muted)" />
              <div>
                <h3>Analysis Results Pending</h3>
                <p style={{ fontSize: '13px', marginTop: '6px' }}>Select patient details, upload a dermatoscopic image, and run the classifier to generate diagnostic probabilities and heatmaps.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
