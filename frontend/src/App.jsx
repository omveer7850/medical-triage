import React, { useState } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import XrayTriage from './components/XrayTriage';
import SkinTriage from './components/SkinTriage';
import TeethTriage from './components/TeethTriage';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const handleScanComplete = () => {
    // When a scan completes, we can switch to the dashboard tab automatically
    // or just let the user stay on the page. Let's switch to dashboard so they see the updated list.
    setActiveTab('dashboard');
  };

  return (
    <div className="app-container">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="app-main">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'xray' && <XrayTriage onScanComplete={handleScanComplete} />}
        {activeTab === 'skin' && <SkinTriage onScanComplete={handleScanComplete} />}
        {activeTab === 'teeth' && <TeethTriage onScanComplete={handleScanComplete} />}
      </main>
      
      <footer style={{ 
        textAlign: 'center', 
        padding: '24px', 
        color: 'var(--color-text-muted)', 
        fontSize: '12px',
        borderTop: '1px solid var(--border-glass)',
        background: 'rgba(5, 7, 12, 0.4)',
        marginTop: 'auto'
      }}>
        MED-TRIAGE AI Decision-Support System &copy; 2026. Explicitly designed for clinical triage prioritization. Not a diagnostic replacement.
      </footer>
    </div>
  );
}

export default App;
