import React, { useState, useEffect } from 'react';

export default function RawFileCarvingView() {
  const [isCarving, setIsCarving] = useState(false);
  const [stats, setStats] = useState({ recovered: 0, valid: 0, partial: 0, invalid: 0 });
  const [logs, setLogs] = useState([{ type: 'READY', text: 'System initialized and ready' }]);
  const [drives, setDrives] = useState({ physical: [], logical: [] });
  const [targetType, setTargetType] = useState('logical'); // 'physical', 'logical', 'image'
  const [selectedTarget, setSelectedTarget] = useState('evidence.img'); // default
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5001/api/drives")
      .then(res => res.json())
      .then(data => {
        setDrives(data);
      })
      .catch(err => console.error("Failed to load drives:", err));
  }, []);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    setIsUploading(true);
    setLogs(prev => [...prev, { type: 'INFO', text: `Uploading ${file.name}...` }]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:5001/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data.success) {
        setSelectedTarget(data.target);
        setLogs(prev => [...prev, { type: 'SUCCESS', text: `Upload complete: ${data.target}` }]);
      } else {
        setLogs(prev => [...prev, { type: 'ERROR', text: `Upload failed: ${data.error}` }]);
      }
    } catch (error) {
      console.error(error);
      setLogs(prev => [...prev, { type: 'ERROR', text: 'Upload failed.' }]);
    } finally {
      setIsUploading(false);
    }
  };

  const handleStartCarving = async () => {
    setIsCarving(true);
    setLogs(prev => [...prev, { type: 'INFO', text: 'Starting raw file carving...' }]);
    
    try {
      const response = await fetch("http://127.0.0.1:5001/api/recover", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ method: "carving", target: selectedTarget })
      });
      
      const data = await response.json();
      
      if (data.status === "success") {
        let valid = 0, partial = 0, invalid = 0;
        data.files.forEach(f => {
          if (f.status === 'VALID') valid++;
          else if (f.status === 'PARTIAL') partial++;
          else invalid++;
        });

        setStats({ 
          recovered: data.total_recovered, 
          valid, 
          partial, 
          invalid,
          files: data.files 
        });

        setLogs(prev => [
          ...prev, 
          { type: 'SUCCESS', text: `Carving complete. ${data.total_recovered} files recovered.` },
          { type: 'VALIDATE', text: 'Validation finished.' }
        ]);
      } else {
        setLogs(prev => [...prev, { type: 'ERROR', text: data.detail || 'Recovery failed.' }]);
      }
    } catch (error) {
      console.error(error);
      setLogs(prev => [...prev, { type: 'ERROR', text: 'Failed to connect to backend engine.' }]);
    } finally {
      setIsCarving(false);
    }
  };

  return (
    <div className="content">
      <div className="page-header">
        <div className="page-title">
          <div>
            <h1>Raw File Carving</h1>
            <p>Recover files directly from disk images without filesystem metadata.</p>
          </div>
        </div>
      </div>

      <div className="main-grid" style={{ marginBottom: '20px' }}>
        
        {/* LEFT COLUMN */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* Control Card */}
          <div className="panel configuration">
            <div className="panel-title">
              <span style={{ color: '#00f0ff' }}>◷</span>
              <h2>Recovery Operations</h2>
            </div>
            
            <div style={{ marginBottom: '1.5rem', color: '#94a3b8', fontSize: '13px' }}>
              Primary Method: <strong style={{ color: '#fff' }}>Raw File Carving</strong> <br />
              Supported Types: <span style={{ fontFamily: 'monospace', color: '#a855f7' }}>PNG, JPG, PDF, DOCX, ZIP</span>
            </div>

            <button 
              className="start-button" 
              onClick={handleStartCarving}
              disabled={isCarving}
              style={{ width: '100%', padding: '15px', background: isCarving ? '#1d3854' : 'linear-gradient(90deg, #00bd8d, #08caa0)', opacity: isCarving ? 0.7 : 1 }}
            >
              <span style={{ fontSize: '15px' }}>{isCarving ? 'Carving in progress...' : '▶ Start Raw Carving'}</span>
            </button>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px', marginTop: '20px' }}>
              <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid #1a334e', borderRadius: '8px', padding: '15px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', fontFamily: 'monospace', color: '#00f0ff' }}>{stats.recovered}</div>
                <div style={{ fontSize: '11px', color: '#879bb5', textTransform: 'uppercase' }}>Recovered</div>
              </div>
              <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid #1a334e', borderRadius: '8px', padding: '15px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', fontFamily: 'monospace', color: '#10b981' }}>{stats.valid}</div>
                <div style={{ fontSize: '11px', color: '#879bb5', textTransform: 'uppercase' }}>Valid</div>
              </div>
              <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid #1a334e', borderRadius: '8px', padding: '15px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', fontFamily: 'monospace', color: '#f59e0b' }}>{stats.partial}</div>
                <div style={{ fontSize: '11px', color: '#879bb5', textTransform: 'uppercase' }}>Partial</div>
              </div>
              <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid #1a334e', borderRadius: '8px', padding: '15px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', fontFamily: 'monospace', color: '#f43f5e' }}>{stats.invalid}</div>
                <div style={{ fontSize: '11px', color: '#879bb5', textTransform: 'uppercase' }}>Invalid</div>
              </div>
            </div>
          </div>

          {/* Recovered Files Table */}
          <div className="panel recent">
            <div className="recent-header">
              <div className="panel-title">
                <span style={{ color: '#a855f7' }}>▣</span>
                <h2>Recovered Files</h2>
              </div>
            </div>
            <table style={{ width: '100%', marginTop: '10px' }}>
              <thead>
                <tr>
                  <th>Filename</th>
                  <th>Type</th>
                  <th>Size</th>
                  <th>Status</th>
                  <th>Hash</th>
                </tr>
              </thead>
              <tbody>
                {stats.recovered > 0 ? (
                  stats.files && stats.files.map((file, idx) => (
                    <tr key={idx}>
                      <td style={{ fontFamily: 'monospace' }}>{file.filename}</td>
                      <td>{file.filename.split('.').pop().toUpperCase()}</td>
                      <td>{file.size_mb} MB</td>
                      <td>
                        <span style={{ color: file.status === 'VALID' ? '#10b981' : file.status === 'PARTIAL' ? '#f59e0b' : '#f43f5e' }}>
                          {file.status}
                        </span>
                      </td>
                      <td style={{ fontFamily: 'monospace', color: '#a855f7' }}>-</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" style={{ textAlign: 'center', padding: '30px', color: '#879bb5' }}>
                      Ready for raw carving. Click "Start Raw Carving" to begin.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

        </section>

        {/* RIGHT COLUMN */}
        <aside className="right-column">
          
          {/* Target Selection Card */}
          <div className="panel side-panel">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h2 style={{ margin: 0 }}><span style={{ color: '#00f0ff' }}>▰</span> &nbsp; Target Selection</h2>
              <span style={{ background: 'rgba(0, 240, 255, 0.1)', color: '#00f0ff', padding: '4px 8px', borderRadius: '4px', fontSize: '11px', border: '1px solid rgba(0,240,255,0.3)', fontWeight: 'bold' }}>READY</span>
            </div>
            
            <div style={{ display: 'flex', gap: '5px', marginBottom: '15px' }}>
              <button 
                onClick={() => { setTargetType('physical'); if(drives.physical.length) setSelectedTarget(drives.physical[0].id); else setSelectedTarget('evidence.img'); }}
                style={{ flex: 1, padding: '8px', fontSize: '11px', background: targetType === 'physical' ? 'rgba(0, 240, 255, 0.2)' : 'transparent', border: `1px solid ${targetType === 'physical' ? '#00f0ff' : '#1a334e'}`, color: '#fff', borderRadius: '4px', cursor: 'pointer' }}>
                Physical Drive
              </button>
              <button 
                onClick={() => { setTargetType('logical'); if(drives.logical.length) setSelectedTarget(drives.logical[0].id); else setSelectedTarget('evidence.img'); }}
                style={{ flex: 1, padding: '8px', fontSize: '11px', background: targetType === 'logical' ? 'rgba(168, 85, 247, 0.2)' : 'transparent', border: `1px solid ${targetType === 'logical' ? '#a855f7' : '#1a334e'}`, color: '#fff', borderRadius: '4px', cursor: 'pointer' }}>
                Logical Volume
              </button>
              <button 
                onClick={() => { setTargetType('image'); setSelectedTarget(''); }}
                style={{ flex: 1, padding: '8px', fontSize: '11px', background: targetType === 'image' ? 'rgba(16, 185, 129, 0.2)' : 'transparent', border: `1px solid ${targetType === 'image' ? '#10b981' : '#1a334e'}`, color: '#fff', borderRadius: '4px', cursor: 'pointer' }}>
                Disk Image
              </button>
            </div>

            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', fontSize: '11px', color: '#879bb5', marginBottom: '5px', textTransform: 'uppercase' }}>
                {targetType === 'image' ? 'Upload Image (.img, .dd)' : 'Select Drive / Volume'}
              </label>
              
              {targetType === 'image' ? (
                <div>
                  <input type="file" id="disk-image-upload" style={{ display: 'none' }} accept=".img,.dd,.iso,.bin" onChange={handleFileUpload} />
                  <button onClick={() => document.getElementById('disk-image-upload').click()} style={{ width: '100%', padding: '10px', background: 'rgba(0,0,0,0.3)', color: '#fff', border: '1px solid #1a334e', borderRadius: '4px', cursor: 'pointer' }}>
                    {isUploading ? 'Uploading...' : 'Browse for Image File...'}
                  </button>
                </div>
              ) : (
                <select 
                  value={selectedTarget}
                  onChange={e => setSelectedTarget(e.target.value)}
                  style={{ width: '100%', padding: '10px', background: 'rgba(0,0,0,0.3)', color: '#fff', border: '1px solid #1a334e', borderRadius: '4px' }}>
                  <option value="evidence.img">Simulated evidence.img</option>
                  {drives[targetType]?.map(d => (
                    <option key={d.id} value={d.id}>{d.name} ({d.size_gb} GB)</option>
                  ))}
                </select>
              )}
            </div>
            
            <div className="drive-details">
              <div>
                <span>Target Path</span>
                <strong style={{ fontFamily: 'monospace', color: '#a855f7', wordBreak: 'break-all' }}>{selectedTarget || 'No file selected'}</strong>
              </div>
              <div>
                <span>Access Level</span>
                <strong style={{ color: '#f59e0b' }}>
                  {targetType === 'physical' ? 'Raw Block Access (Admin)' : targetType === 'logical' ? 'Filesystem Level' : 'Image File Parsing'}
                </strong>
              </div>
            </div>
          </div>

          {/* Operation Logs */}
          <div className="panel side-panel">
            <h2><span style={{ color: '#f59e0b' }}>▤</span> &nbsp; Operation Logs</h2>
            <div style={{ 
              background: 'rgba(0,0,0,0.5)', 
              border: '1px solid #1a334e', 
              borderRadius: '6px', 
              padding: '15px', 
              height: '250px', 
              overflowY: 'auto',
              fontFamily: 'monospace',
              fontSize: '12px',
              lineHeight: '1.6'
            }}>
              {logs.map((log, i) => (
                <div key={i} style={{ marginBottom: '8px', paddingBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <span style={{ color: '#00f0ff' }}>[{log.type}]</span> {log.text}
                </div>
              ))}
            </div>

            <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #1a334e' }}>
              <div className="drive-details">
                <div>
                  <span>Signatures Detected</span>
                  <strong style={{ color: '#a855f7' }}>{stats.recovered}</strong>
                </div>
                <div>
                  <span>Output Directory</span>
                  <strong>/recovered</strong>
                </div>
              </div>
            </div>
          </div>

        </aside>

      </div>
    </div>
  );
}
