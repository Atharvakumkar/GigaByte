import React from 'react';

export default function Topbar() {
  return (
    <header className="topbar">
      <div className="search">
        <span>⌕</span>
        <input
          placeholder="Search drives, devices, or operations..."
        />
      </div>

      <div className="profile-area">
        <div className="notification">
          ♧
          <span></span>
        </div>

        <div className="profile-circle">
          AK
        </div>

        <div className="profile-text">
          <strong>Atharva Kumkar</strong>
          <small>Investigator</small>
        </div>

        <div className="profile-arrow">
          ⌄
        </div>
      </div>
    </header>
  );
}
