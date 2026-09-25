import "./App.css";
import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import SanitizationView from "./views/SanitizationView";
import AnalysisVerificationView from "./views/AnalysisVerificationView";
import AuditTrailView from "./views/AuditTrailView";
import ReportsCertificatesView from "./views/ReportsCertificatesView";
import PlaceholderView from "./views/PlaceholderView";
import RawFileCarvingView from "./views/RawFileCarvingView";

function App() {
  const [activeTab, setActiveTab] = useState("Data Sanitization");

  const renderContent = () => {
    switch (activeTab) {
      case "Data Sanitization":
        return <SanitizationView />;
      case "Analysis & Verification":
        return <AnalysisVerificationView />;
      case "Audit Trail":
        return <AuditTrailView />;
      case "Reports & Certificates":
        return <ReportsCertificatesView />;
      case "Raw File Carving":
        return <RawFileCarvingView />;
      default:
        return <PlaceholderView title={activeTab} />;
    }
  };

  return (
    <div className="app">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="main">
        <Topbar />
        {renderContent()}
      </main>
    </div>
  );
}

export default App;