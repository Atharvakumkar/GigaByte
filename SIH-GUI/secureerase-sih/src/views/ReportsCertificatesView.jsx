import React from 'react';

export default function ReportsCertificatesView() {
  const certData = {
    targetName: "evidence.img",
    targetHash: "f2c4b8d13b8a1c9ea9d3e4f7...",
    filesystem: "NTFS",
    pre_identified: 3,
    pre_recovered: 3,
    pre_validated: 2,
    confidence: "76%",
    recoverability: "76%",
    san_method: "NIST 800-88 (Clear)",
    san_status: "COMPLETED",
    san_timestamp: "2026-09-24T10:20:00Z",
    post_recovered: 0,
    post_previously_identified: 0,
    verification: "PASS",
    audit_integrity: "VALID",
    final_status: "SANITIZATION: VERIFIED"
  };

  const downloadJson = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(certData, null, 2));
    const dlAnchorElem = document.createElement('a');
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", "sanitization_certificate.json");
    dlAnchorElem.click();
  };

  return (
    <div className="content">
      <div className="page-header">
        <div className="page-title">
          <div>
            <h1>Reports & Certificates</h1>
            <p>Generate and export formal sanitization evidence.</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={() => alert('PDF generation would trigger here.')} className="audit-button" style={{ background: '#0b2036', color: '#16a7ff' }}>
            ▤ &nbsp; Download PDF
          </button>
          <button onClick={downloadJson} className="audit-button" style={{ background: '#0b2036', color: '#16a7ff' }}>
            {'{ }'} &nbsp; Download JSON
          </button>
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <div className="panel" style={{ width: '800px', padding: '40px', fontFamily: 'monospace', color: '#c7d5e5', border: '1px solid #2c6f9c', background: '#061221' }}>
          <div style={{ textAlign: 'center', marginBottom: '30px' }}>
            <h1 style={{ color: '#00d8a1', letterSpacing: '2px', fontSize: '24px' }}>SANITIZATION CERTIFICATE</h1>
            <div style={{ color: '#879bb5' }}>==================================================</div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ color: '#a855f7', marginBottom: '5px' }}>TARGET INFORMATION</h3>
            <div>Target Name      : {certData.targetName}</div>
            <div>Target SHA-256   : {certData.targetHash}</div>
            <div>Filesystem       : {certData.filesystem}</div>
          </div>

          <div style={{ color: '#879bb5', marginBottom: '20px' }}>--------------------------------------------------</div>

          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ color: '#a855f7', marginBottom: '5px' }}>PRE-SANITIZATION BASELINE</h3>
            <div>Files Identified : {certData.pre_identified}</div>
            <div>Files Recovered  : {certData.pre_recovered}</div>
            <div>Files Validated  : {certData.pre_validated}</div>
            <div>Avg Confidence   : {certData.confidence}</div>
            <div>Recoverability   : {certData.recoverability}</div>
          </div>

          <div style={{ color: '#879bb5', marginBottom: '20px' }}>--------------------------------------------------</div>

          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ color: '#a855f7', marginBottom: '5px' }}>SANITIZATION OPERATION</h3>
            <div>Method Used      : {certData.san_method}</div>
            <div>Status           : {certData.san_status}</div>
            <div>Timestamp        : {certData.san_timestamp}</div>
          </div>

          <div style={{ color: '#879bb5', marginBottom: '20px' }}>--------------------------------------------------</div>

          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ color: '#a855f7', marginBottom: '5px' }}>POST-SANITIZATION RECOVERY</h3>
            <div>Total Recovered  : {certData.post_recovered}</div>
            <div>Previous Found   : {certData.post_previously_identified} (0 is required for PASS)</div>
          </div>

          <div style={{ color: '#879bb5', marginBottom: '30px' }}>==================================================</div>

          <div style={{ textAlign: 'center', marginBottom: '20px', display: 'flex', justifyContent: 'center', gap: '20px' }}>
            <div style={{ padding: '10px 20px', border: '1px solid #00d6a0', background: '#0a3035', color: '#00e4aa', borderRadius: '5px', fontWeight: 'bold' }}>
              VERIFICATION: {certData.verification}
            </div>
            <div style={{ padding: '10px 20px', border: '1px solid #00d6a0', background: '#0a3035', color: '#00e4aa', borderRadius: '5px', fontWeight: 'bold' }}>
              AUDIT: {certData.audit_integrity}
            </div>
          </div>

          <div style={{ textAlign: 'center', fontSize: '20px', fontWeight: 'bold', color: '#00d8a1', marginTop: '30px' }}>
            {certData.final_status}
          </div>
        </div>
      </div>
    </div>
  );
}
