import React, { useState } from 'react';

// Dummy data for baseline
const baselineArtifacts = [
  { file_name: "document_1.docx", file_type: "DOCX", source_image: "evidence.img", offset: "0x1A2B00", size: "24 KB", recovery_method: "Filesystem", validation_status: "VALID", confidence_score: 95, sha256: "3b8a1c9e...", checks: { sig: 1, struct: 1, parser: 1, fs: 1, integrity: 1 } },
  { file_name: "image_hidden.jpg", file_type: "JPG", source_image: "evidence.img", offset: "0x3F8000", size: "1.2 MB", recovery_method: "Raw Carving", validation_status: "VALID", confidence_score: 80, sha256: "f2c4b8d1...", checks: { sig: 1, struct: 1, parser: 1, fs: 0, integrity: 1 } },
  { file_name: "config_backup.zip", file_type: "ZIP", source_image: "evidence.img", offset: "0x5A0000", size: "5 MB", recovery_method: "Reconstruction", validation_status: "PARTIAL", confidence_score: 55, sha256: "a9d3e4f7...", checks: { sig: 1, struct: 0, parser: 1, fs: 0, integrity: 0 } },
];

// After sanitization
const postSanitizationArtifacts = [
  // empty array means all artifacts were destroyed, PASS
];

export default function AnalysisVerificationView() {
  const [selectedFile, setSelectedFile] = useState(null);

  // Confidence score formula: valid_signature=30%, valid_structure=25%, parser_passed=25%, filesystem_evidence=20%
  const calculateScore = (checks) => {
    return (checks.sig * 30) + (checks.struct * 25) + (checks.parser * 25) + (checks.fs * 20);
  };

  const avgRecoverability = baselineArtifacts.reduce((acc, curr) => acc + calculateScore(curr.checks), 0) / baselineArtifacts.length;
  const passVerification = postSanitizationArtifacts.length === 0;

  return (
    <div className="content">
      <div className="page-header">
        <div className="page-title">
          <div>
            <h1>Analysis & Verification</h1>
            <p>Measure recovery confidence and verify sanitization.</p>
          </div>
        </div>
      </div>

      <div className="main-grid">
        <section>
          {/* Baseline Comparison */}
          <div className="panel configuration" style={{ marginBottom: '18px' }}>
            <div className="panel-title">
              <span>◆</span>
              <h2>Pre/Post-Sanitization Comparison</h2>
            </div>
            
            <div style={{ display: 'flex', gap: '20px' }}>
              <div style={{ flex: 1 }}>
                <h3 style={{ color: '#a9c4e4', fontSize: '14px', marginBottom: '10px' }}>Before Sanitization</h3>
                <table style={{ width: '100%', fontSize: '11px' }}>
                  <thead>
                    <tr>
                      <th style={{ textAlign: 'left', color: '#879bb5', borderBottom: '1px solid #1d334b', padding: '8px' }}>Artifact</th>
                      <th style={{ textAlign: 'left', color: '#879bb5', borderBottom: '1px solid #1d334b', padding: '8px' }}>Type</th>
                      <th style={{ textAlign: 'left', color: '#879bb5', borderBottom: '1px solid #1d334b', padding: '8px' }}>Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {baselineArtifacts.map((art, idx) => (
                      <tr key={idx} onClick={() => setSelectedFile(art)} style={{ cursor: 'pointer', background: selectedFile === art ? '#0a3035' : 'transparent' }}>
                        <td style={{ padding: '8px', borderBottom: '1px solid #152a40', fontFamily: 'monospace' }}>{art.file_name}</td>
                        <td style={{ padding: '8px', borderBottom: '1px solid #152a40' }}>{art.file_type}</td>
                        <td style={{ padding: '8px', borderBottom: '1px solid #152a40' }}>
                          <span style={{ color: '#00d8a1' }}>{calculateScore(art.checks)}%</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div style={{ flex: 1 }}>
                <h3 style={{ color: '#a9c4e4', fontSize: '14px', marginBottom: '10px' }}>After Sanitization</h3>
                <table style={{ width: '100%', fontSize: '11px' }}>
                  <thead>
                    <tr>
                      <th style={{ textAlign: 'left', color: '#879bb5', borderBottom: '1px solid #1d334b', padding: '8px' }}>Artifact</th>
                      <th style={{ textAlign: 'left', color: '#879bb5', borderBottom: '1px solid #1d334b', padding: '8px' }}>Recoverable?</th>
                    </tr>
                  </thead>
                  <tbody>
                    {baselineArtifacts.map((art, idx) => {
                      const survived = postSanitizationArtifacts.find(p => p.sha256 === art.sha256);
                      return (
                        <tr key={idx}>
                          <td style={{ padding: '8px', borderBottom: '1px solid #152a40', fontFamily: 'monospace', opacity: survived ? 1 : 0.5 }}>{art.file_name}</td>
                          <td style={{ padding: '8px', borderBottom: '1px solid #152a40' }}>
                            {survived ? <span style={{ color: '#00d8a1' }}>✓ Yes</span> : <span style={{ color: '#ff626b' }}>✗ No</span>}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            <div style={{ marginTop: '20px', padding: '15px', background: passVerification ? '#0a3035' : '#281b2a', border: `1px solid ${passVerification ? '#00d6a0' : '#ff626b'}`, borderRadius: '7px', textAlign: 'center' }}>
              <h2 style={{ color: passVerification ? '#00e4aa' : '#ff737a', margin: '0 0 10px', fontSize: '20px' }}>
                VERIFICATION: {passVerification ? 'PASS' : 'FAIL'}
              </h2>
              <p style={{ color: passVerification ? '#a9eccf' : '#ffb6b9', margin: 0, fontSize: '13px' }}>
                {passVerification 
                  ? "No previously identified artifacts were recovered under the defined verification procedure."
                  : "Some previously identified artifacts remain recoverable. Sanitization failed."}
              </p>
            </div>
          </div>
        </section>

        <aside className="right-column">
          {/* Recoverability Score */}
          <div className="panel side-panel">
            <h2>◷ &nbsp; Recoverability Score</h2>
            <div className="progress-circle">
              <div>
                <strong>{avgRecoverability.toFixed(0)}%</strong>
                <span>Overall Score</span>
              </div>
            </div>
            <p style={{ fontSize: '12px', color: '#a6b6cb', textAlign: 'center', marginTop: '10px' }}>
              Average confidence score across all {baselineArtifacts.length} recoverable artifacts prior to sanitization.
            </p>
          </div>

          {/* Recovery Confidence */}
          <div className="panel side-panel" style={{ opacity: selectedFile ? 1 : 0.5 }}>
            <h2>◆ &nbsp; Recovery Confidence</h2>
            {selectedFile ? (
              <div>
                <p style={{ fontFamily: 'monospace', fontSize: '13px', color: '#d3e0f0', marginBottom: '15px' }}>{selectedFile.file_name}</p>
                <div className="verification-list">
                  <div>
                    <span className="verify-check" style={{ color: selectedFile.checks.sig ? '#00e4aa' : '#ff626b' }}>
                      {selectedFile.checks.sig ? '✓' : '✗'}
                    </span>
                    Valid Signature (30%)
                  </div>
                  <div>
                    <span className="verify-check" style={{ color: selectedFile.checks.struct ? '#00e4aa' : '#ff626b' }}>
                      {selectedFile.checks.struct ? '✓' : '✗'}
                    </span>
                    Valid Structure (25%)
                  </div>
                  <div>
                    <span className="verify-check" style={{ color: selectedFile.checks.parser ? '#00e4aa' : '#ff626b' }}>
                      {selectedFile.checks.parser ? '✓' : '✗'}
                    </span>
                    Parser Validation (25%)
                  </div>
                  <div>
                    <span className="verify-check" style={{ color: selectedFile.checks.fs ? '#00e4aa' : '#ff626b' }}>
                      {selectedFile.checks.fs ? '✓' : '✗'}
                    </span>
                    Filesystem Evidence (20%)
                  </div>
                </div>
                <div className="progress-bar" style={{ marginTop: '20px', background: '#1d3854' }}>
                  <div className="progress-fill started completed" style={{ width: `${calculateScore(selectedFile.checks)}%`, background: '#06b6d4' }}></div>
                </div>
                <div style={{ textAlign: 'right', fontSize: '11px', color: '#06b6d4', marginTop: '5px' }}>
                  Confidence Score: {calculateScore(selectedFile.checks)}%
                </div>
              </div>
            ) : (
              <p style={{ fontSize: '12px', color: '#899bb3', padding: '20px 0', textAlign: 'center' }}>
                Select an artifact to view its confidence breakdown.
              </p>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}
