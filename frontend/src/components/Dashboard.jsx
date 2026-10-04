import React, { useState, useEffect } from 'react';
import { getReports, getPatients, createPatient, addDoctorNotes } from '../utils/api';
import { User, Users, ShieldAlert, CheckCircle, Plus, Calendar, Search, UserPlus, Layers } from 'lucide-react';

export default function Dashboard() {
  const [reports, setReports] = useState([]);
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedReport, setSelectedReport] = useState(null);
  
  // Registration Form State
  const [regName, setRegName] = useState('');
  const [regAge, setRegAge] = useState('');
  const [regGender, setRegGender] = useState('Male');
  const [regStatus, setRegStatus] = useState('');

  // Doctor Notes State
  const [notes, setNotes] = useState('');
  const [notesSaving, setNotesSaving] = useState(false);

  // Search Filter State
  const [searchQuery, setSearchQuery] = useState('');

  const fetchData = async () => {
    try {
      setLoading(true);
      const repData = await getReports();
      const patData = await getPatients();
      setReports(repData || []);
      setPatients(patData || []);
    } catch (err) {
      console.error("Error fetching dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRegisterPatient = async (e) => {
    e.preventDefault();
    if (!regName || !regAge || !regGender) return;
    try {
      setRegStatus('Registering...');
      const newPat = await createPatient({
        name: regName,
        age: parseInt(regAge),
        gender: regGender
      });
      setRegStatus(`Successfully Registered: ${newPat.patientId}`);
      setRegName('');
      setRegAge('');
      setRegGender('Male');
      fetchData(); // reload list
      setTimeout(() => setRegStatus(''), 4000);
    } catch (err) {
      setRegStatus(`Failed: ${err.message}`);
    }
  };

  const handleSelectReport = (report) => {
    setSelectedReport(report);
    setNotes(report.doctorNotes || '');
  };

  const handleSaveNotes = async (e) => {
    e.preventDefault();
    if (!selectedReport) return;
    try {
      setNotesSaving(true);
      const updated = await addDoctorNotes(selectedReport._id, { doctorNotes: notes });
      setSelectedReport(updated);
      setReports(reports.map(r => r._id === updated._id ? updated : r));
      setNotesSaving(false);
    } catch (err) {
      alert("Error saving notes: " + err.message);
      setNotesSaving(false);
    }
  };

  // Find patient name for a patientId
  const getPatientDetails = (patId) => {
    const p = patients.find(p => p.patientId === patId);
    return p ? `${p.name} (${p.gender}, Age ${p.age})` : patId;
  };

  // Compute Stats
  const totalScans = reports.length;
  const highRiskCount = reports.filter(r => r.severity === 'High').length;
  const pendingCount = reports.filter(r => r.status === 'Pending Review').length;

  // Filtered reports
  const filteredReports = reports.filter(r => {
    const patDetails = getPatientDetails(r.patientId).toLowerCase();
    const disease = r.topPrediction?.disease?.toLowerCase() || '';
    const status = r.status.toLowerCase();
    const query = searchQuery.toLowerCase();
    return patDetails.includes(query) || disease.includes(query) || status.includes(query);
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <h1 className="page-title">Clinical Triage & Diagnostics Dashboard</h1>
      
      {/* Stats Cards */}
      <div className="stats-row">
        <div className="glass-card stat-card">
          <div className="stat-icon">
            <Users size={22} />
          </div>
          <div>
            <div style={{ color: 'var(--color-text-secondary)', fontSize: '14px' }}>Total Scans Queue</div>
            <div className="stat-val">{totalScans}</div>
          </div>
        </div>
        <div className="glass-card stat-card">
          <div className="stat-icon purple" style={{ color: 'var(--color-high)', background: 'rgba(239, 68, 68, 0.1)' }}>
            <ShieldAlert size={22} />
          </div>
          <div>
            <div style={{ color: 'var(--color-text-secondary)', fontSize: '14px' }}>High Risk Flags</div>
            <div className="stat-val" style={{ color: 'var(--color-high)' }}>{highRiskCount}</div>
          </div>
        </div>
        <div className="glass-card stat-card">
          <div className="stat-icon pink" style={{ color: 'var(--color-medium)', background: 'rgba(245, 158, 11, 0.1)' }}>
            <CheckCircle size={22} />
          </div>
          <div>
            <div style={{ color: 'var(--color-text-secondary)', fontSize: '14px' }}>Pending Triage Review</div>
            <div className="stat-val" style={{ color: 'var(--color-medium)' }}>{pendingCount}</div>
          </div>
        </div>
      </div>

      <div className="triage-grid">
        {/* Left Side: Register Patient & Triage Queue */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          {/* Register Patient Form */}
          <div className="glass-card">
            <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <UserPlus size={18} color="var(--color-primary)" />
              Register New Patient
            </h3>
            <form onSubmit={handleRegisterPatient} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr auto', gap: '12px', alignItems: 'end' }}>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label>Name</label>
                <input 
                  type="text" 
                  value={regName} 
                  onChange={(e) => setRegName(e.target.value)} 
                  placeholder="John Doe" 
                  className="form-control"
                  required 
                />
              </div>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label>Age</label>
                <input 
                  type="number" 
                  value={regAge} 
                  onChange={(e) => setRegAge(e.target.value)} 
                  placeholder="34" 
                  className="form-control"
                  required 
                />
              </div>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label>Gender</label>
                <select 
                  value={regGender} 
                  onChange={(e) => setRegGender(e.target.value)} 
                  className="form-control"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <button type="submit" className="btn-glow" style={{ padding: '10px 16px' }}>
                <Plus size={16} style={{ marginRight: '4px' }} /> Register
              </button>
            </form>
            {regStatus && (
              <div style={{ marginTop: '12px', fontSize: '13px', color: regStatus.startsWith('Fail') ? 'var(--color-high)' : 'var(--color-low)' }}>
                {regStatus}
              </div>
            )}
          </div>

          {/* Triage Queue */}
          <div className="glass-card" style={{ flex: 1 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h3>Triage Diagnostics Queue</h3>
              
              <div style={{ position: 'relative' }}>
                <input 
                  type="text" 
                  placeholder="Search scans..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="form-control"
                  style={{ paddingLeft: '32px', fontSize: '13px', width: '200px' }}
                />
                <Search size={14} style={{ position: 'absolute', left: '10px', top: '12px', color: 'var(--color-text-muted)' }} />
              </div>
            </div>
            
            {loading ? (
              <div style={{ padding: '40px 0', textAlignment: 'center', color: 'var(--color-text-secondary)' }}>Loading triage queue...</div>
            ) : filteredReports.length === 0 ? (
              <div style={{ padding: '40px 0', textAlign: 'center', color: 'var(--color-text-muted)', fontSize: '14px' }}>
                No scans found matching filters.
              </div>
            ) : (
              <div style={{ overflowX: 'auto' }}>
                <table className="patient-table">
                  <thead>
                    <tr>
                      <th>Patient</th>
                      <th>Scan Type</th>
                      <th>Top Detection</th>
                      <th>Severity</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredReports.map((report) => (
                      <tr 
                        key={report._id} 
                        onClick={() => handleSelectReport(report)}
                        style={{ background: selectedReport?._id === report._id ? 'rgba(0, 242, 254, 0.05)' : '' }}
                      >
                        <td style={{ fontWeight: '500' }}>
                          {getPatientDetails(report.patientId)}
                          <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', marginTop: '2px' }}>{report.patientId}</div>
                        </td>
                        <td>
                          <span style={{ textTransform: 'uppercase', fontSize: '12px', color: 'var(--color-primary)', fontWeight: 600 }}>
                            {report.scanType === 'xray' ? 'Chest X-Ray' : report.scanType === 'skin' ? 'Skin Lesion' : 'Dental Scan'}
                          </span>
                        </td>
                        <td>
                          <div style={{ fontWeight: '500' }}>{report.topPrediction?.disease || 'N/A'}</div>
                          <div style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>
                            {report.topPrediction ? `${(report.topPrediction.probability * 100).toFixed(1)}%` : ''}
                          </div>
                        </td>
                        <td>
                          <span className={`badge ${report.severity.toLowerCase()}`}>{report.severity}</span>
                        </td>
                        <td>
                          <span style={{ 
                            fontSize: '12px', 
                            color: report.status === 'Reviewed' ? 'var(--color-low)' : 'var(--color-medium)',
                            fontWeight: '600'
                          }}>
                            {report.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* Right Side: Selected Report Details */}
        <div>
          {selectedReport ? (
            <div className="glass-card" style={{ border: `1px solid ${selectedReport.severity === 'High' ? 'rgba(239, 68, 68, 0.3)' : selectedReport.severity === 'Medium' ? 'rgba(245, 158, 11, 0.3)' : 'rgba(255, 255, 255, 0.08)'}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <div>
                  <span className={`badge ${selectedReport.severity.toLowerCase()}`} style={{ marginBottom: '8px' }}>
                    {selectedReport.severity} Severity Case
                  </span>
                  <h2>Diagnostic Report</h2>
                  <div style={{ fontSize: '13px', color: 'var(--color-text-secondary)', marginTop: '4px' }}>
                    Patient: {getPatientDetails(selectedReport.patientId)} | {selectedReport.patientId}
                  </div>
                </div>
                <button 
                  onClick={() => setSelectedReport(null)}
                  style={{ background: 'transparent', border: 'none', color: 'var(--color-text-muted)', cursor: 'pointer', fontSize: '20px' }}
                >
                  &times;
                </button>
              </div>

              {/* Side-by-side Original vs Grad-CAM Overlay */}
              {selectedReport.visualExplainability && (
                <div style={{ marginBottom: '20px' }}>
                  <div style={{ fontSize: '13px', fontWeight: '500', color: 'var(--color-text-secondary)', marginBottom: '8px' }}>
                    Explainable AI (Grad-CAM overlays target layer for disease focus):
                  </div>
                  <div className="image-display-grid" style={{ gridTemplateColumns: '1fr' }}>
                    <div className="image-box" style={{ aspectRatio: '1.6/1', height: '240px' }}>
                      <img src={selectedReport.visualExplainability} alt="Grad-CAM Overlay" />
                      <div className="image-label">Grad-CAM Overlay: {selectedReport.visualizedClass}</div>
                    </div>
                  </div>
                </div>
              )}

              {/* Predictions Table */}
              <div style={{ marginBottom: '20px' }}>
                <h4 style={{ marginBottom: '10px' }}>AI Prediction Probabilities</h4>
                <div className="prediction-list" style={{ maxHeight: '180px', overflowY: 'auto', paddingRight: '6px' }}>
                  {selectedReport.predictions
                    .slice()
                    .sort((a, b) => b.probability - a.probability)
                    .map((pred, i) => (
                      <div key={i} className="prediction-row">
                        <div className="prediction-label">
                          <span>{pred.disease}</span>
                          <span style={{ fontWeight: '600' }}>{(pred.probability * 100).toFixed(2)}%</span>
                        </div>
                        <div className="prediction-bar-bg">
                          <div 
                            className={`prediction-bar-fill ${selectedReport.scanType === 'skin' ? 'accent' : selectedReport.scanType === 'teeth' ? 'teeth' : ''}`}
                            style={{ width: `${pred.probability * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                </div>
              </div>

              {/* Doctor Notes Form */}
              <form onSubmit={handleSaveNotes}>
                <div className="form-group">
                  <label>Clinical Notes / Actions (Marks as Reviewed)</label>
                  <textarea 
                    value={notes} 
                    onChange={(e) => setNotes(e.target.value)} 
                    placeholder="Enter diagnosis validation, recommended next specialist steps, or notes..." 
                    className="form-control"
                    required
                  />
                </div>
                <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                  <button 
                    type="submit" 
                    className="btn-glow" 
                    disabled={notesSaving}
                    style={{ background: selectedReport.status === 'Reviewed' ? 'rgba(255, 255, 255, 0.1)' : '', color: selectedReport.status === 'Reviewed' ? '#fff' : '', boxShadow: selectedReport.status === 'Reviewed' ? 'none' : '' }}
                  >
                    {notesSaving ? 'Saving...' : selectedReport.status === 'Reviewed' ? 'Update Notes' : 'Mark Reviewed & Save'}
                  </button>
                </div>
              </form>
            </div>
          ) : (
            <div className="glass-card" style={{ textAlign: 'center', padding: '80px 20px', color: 'var(--color-text-muted)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '12px' }}>
              <Layers size={40} strokeWidth={1.5} color="var(--color-text-muted)" />
              <div>
                <h3>No Scans Selected</h3>
                <p style={{ fontSize: '13px', marginTop: '6px' }}>Select any diagnosis case from the left list to review detailed scan inputs, view Grad-CAM heatmaps, and write clinical notes.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
