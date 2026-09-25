import React from 'react';

export default function PlaceholderView({ title }) {
  return (
    <div className="content">
      <div className="page-header">
        <div className="page-title">
          <div>
            <h1>{title}</h1>
            <p>This module is currently under development or exists in another repository.</p>
          </div>
        </div>
      </div>
      
      <div className="panel" style={{ padding: '40px', textAlign: 'center', marginTop: '20px' }}>
        <h2 style={{ color: '#879bb5' }}>Module: {title}</h2>
        <p style={{ color: '#a6b6cb' }}>Backend integration pending.</p>
      </div>
    </div>
  );
}
