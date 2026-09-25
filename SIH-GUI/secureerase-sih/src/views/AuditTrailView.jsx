import React, { useState, useEffect } from 'react';

const initialEvents = [
  { id: 1, timestamp: "2026-09-24T10:00:00Z", type: "IMAGE_MOUNT", details: "Mounted evidence.img", prev_hash: "00000000000000000000000000000000", hash: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6" },
  { id: 2, timestamp: "2026-09-24T10:05:00Z", type: "RECOVERY_START", details: "Started File Carving", prev_hash: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6", hash: "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6a1" },
  { id: 3, timestamp: "2026-09-24T10:20:00Z", type: "SANITIZATION_START", details: "Started NIST 800-88", prev_hash: "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6a1", hash: "c3d4e5f6g7h8i9j0k1l2m3n4o5p6a1b2" },
  { id: 4, timestamp: "2026-09-24T10:25:00Z", type: "VERIFICATION_PASS", details: "No artifacts recovered", prev_hash: "c3d4e5f6g7h8i9j0k1l2m3n4o5p6a1b2", hash: "d4e5f6g7h8i9j0k1l2m3n4o5p6a1b2c3" },
];

// Simple hash simulation for demo purposes
const computeHash = (dataStr, prevHash) => {
  let hash = 0;
  const str = dataStr + prevHash;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(16).padStart(32, '0');
};

export default function AuditTrailView() {
  const [events, setEvents] = useState(initialEvents);
  const [verificationResult, setVerificationResult] = useState(null); // null, {valid: true}, {valid: false, brokenAt: id}
  const [devToolsOpen, setDevToolsOpen] = useState(false);
  const [tamperTargetId, setTamperTargetId] = useState(2);
  const [tamperDetails, setTamperDetails] = useState("Started File Carving [TAMPERED]");

  // We actually initialize the hashes correctly based on the mock function so verification passes initially
  useEffect(() => {
    let currentEvents = [...initialEvents];
    for (let i = 0; i < currentEvents.length; i++) {
      const e = currentEvents[i];
      const dataStr = e.timestamp + e.type + e.details;
      if (i === 0) {
        e.hash = computeHash(dataStr, e.prev_hash);
      } else {
        e.prev_hash = currentEvents[i-1].hash;
        e.hash = computeHash(dataStr, e.prev_hash);
      }
    }
    setEvents(currentEvents);
  }, []);

  const verifyChain = () => {
    for (let i = 0; i < events.length; i++) {
      const e = events[i];
      const dataStr = e.timestamp + e.type + e.details;
      const expectedPrevHash = i === 0 ? "00000000000000000000000000000000" : events[i-1].hash;
      const expectedHash = computeHash(dataStr, expectedPrevHash);

      if (e.prev_hash !== expectedPrevHash || e.hash !== expectedHash) {
        setVerificationResult({ valid: false, brokenAt: e.id });
        return;
      }
    }
    setVerificationResult({ valid: true });
  };

  const handleTamper = () => {
    const updatedEvents = [...events];
    const index = updatedEvents.findIndex(e => e.id === tamperTargetId);
    if (index !== -1) {
      updatedEvents[index].details = tamperDetails;
      setEvents(updatedEvents);
      setVerificationResult(null);
    }
  };

  return (
    <div className="content">
      <div className="page-header">
        <div className="page-title">
          <div>
            <h1>Tamper-Evident Audit Trail</h1>
            <p>Chronological event log with cryptographic chain of custody.</p>
          </div>
        </div>
        <button className="audit-button" onClick={verifyChain} style={{ background: 'linear-gradient(90deg, #00bd8d, #08caa0)', color: 'white', border: 'none' }}>
          ◆ &nbsp; Verify Chain Integrity
        </button>
      </div>

      {verificationResult && (
        <div style={{ marginBottom: '20px', padding: '15px', background: verificationResult.valid ? '#0a3035' : '#281b2a', border: `1px solid ${verificationResult.valid ? '#00d6a0' : '#ff626b'}`, borderRadius: '7px', textAlign: 'center' }}>
          <h2 style={{ color: verificationResult.valid ? '#00e4aa' : '#ff737a', margin: '0', fontSize: '20px' }}>
            {verificationResult.valid ? 'AUDIT INTEGRITY: VALID' : `AUDIT INTEGRITY: BROKEN AT EVENT #${verificationResult.brokenAt}`}
          </h2>
        </div>
      )}

      <div className="panel recent">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Event Type</th>
              <th>Details</th>
              <th>Hash</th>
              <th>Prev Hash</th>
            </tr>
          </thead>
          <tbody>
            {events.map((e) => (
              <tr key={e.id}>
                <td style={{ fontFamily: 'monospace' }}>{e.timestamp}</td>
                <td><span className="status" style={{ color: '#06b6d4' }}>{e.type}</span></td>
                <td>{e.details}</td>
                <td style={{ fontFamily: 'monospace', color: '#a855f7' }}>{e.hash}</td>
                <td style={{ fontFamily: 'monospace', color: '#879bb5' }}>{e.prev_hash}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ marginTop: '30px' }}>
        <button 
          onClick={() => setDevToolsOpen(!devToolsOpen)}
          style={{ background: 'transparent', color: '#879bb5', border: '1px dashed #203a55', padding: '5px 10px', borderRadius: '5px' }}
        >
          {devToolsOpen ? "Hide Dev Tools" : "Show Dev Tools (Demo Only)"}
        </button>

        {devToolsOpen && (
          <div className="panel" style={{ marginTop: '10px', padding: '15px', background: '#0b1626' }}>
            <h3 style={{ margin: '0 0 10px', fontSize: '14px', color: '#a855f7' }}>Tamper Event Data</h3>
            <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
              <select value={tamperTargetId} onChange={(e) => setTamperTargetId(parseInt(e.target.value))} style={{ padding: '5px', background: '#0a1b2e', color: 'white', border: '1px solid #203a58' }}>
                {events.map(e => <option key={e.id} value={e.id}>Event #{e.id}</option>)}
              </select>
              <input 
                type="text" 
                value={tamperDetails} 
                onChange={(e) => setTamperDetails(e.target.value)}
                style={{ padding: '5px', background: '#0a1b2e', color: 'white', border: '1px solid #203a58', flex: 1 }}
              />
              <button onClick={handleTamper} style={{ background: '#ff626b', color: 'white', border: 'none', padding: '5px 15px', borderRadius: '4px' }}>Simulate Tamper</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
