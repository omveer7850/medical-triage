import React from 'react';
import { Activity, ShieldAlert, Layers, UserPlus, Smile } from 'lucide-react';

export default function Header({ activeTab, setActiveTab }) {
  return (
    <header className="header-glass">
      <div className="brand">
        <Activity className="brand-logo-icon" size={28} color="#00f2fe" />
        <span className="brand-logo-text">MED-TRIAGE AI</span>
      </div>
      
      <nav className="nav-links">
        <button 
          onClick={() => setActiveTab('dashboard')} 
          className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
        >
          <Layers size={16} />
          <span>Triage Board</span>
        </button>
        <button 
          onClick={() => setActiveTab('xray')} 
          className={`nav-btn ${activeTab === 'xray' ? 'active' : ''}`}
        >
          <ShieldAlert size={16} />
          <span>Chest X-Ray</span>
        </button>
        <button 
          onClick={() => setActiveTab('skin')} 
          className={`nav-btn ${activeTab === 'skin' ? 'active' : ''}`}
        >
          <Activity size={16} />
          <span>Skin Lesion</span>
        </button>
        <button 
          onClick={() => setActiveTab('teeth')} 
          className={`nav-btn ${activeTab === 'teeth' ? 'active' : ''}`}
        >
          <Smile size={16} />
          <span>Dental Scan</span>
        </button>
      </nav>
    </header>
  );
}
