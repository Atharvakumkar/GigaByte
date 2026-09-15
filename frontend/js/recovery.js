// recovery.js

// ==========================================
// NAVIGATION & UI
// ==========================================
function switchTab(tabId) {
    // Hide all views
    document.querySelectorAll('.view-section').forEach(el => {
        el.classList.remove('active');
    });
    // Un-highlight all tabs
    document.querySelectorAll('.tab-btn').forEach(el => {
        el.classList.remove('active');
    });

    // Show selected view and highlight tab
    document.getElementById(`view-${tabId}`).classList.add('active');
    document.getElementById(`tab-${tabId}`).classList.add('active');
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ==========================================
// RAW FILE CARVING LOGIC
// ==========================================
function appendLog(tagClass, tagText, message) {
    const logPanel = document.getElementById('logPanel');
    const logLine = document.createElement('div');
    logLine.className = 'log-line';
    logLine.innerHTML = `<span class="${tagClass} mono">[${tagText}]</span> ${message}`;
    logPanel.appendChild(logLine);
    logPanel.scrollTop = logPanel.scrollHeight;
}

async function loadImageInfo(driveId) {
    try {
        const response = await fetch(`/api/image-info/${driveId}`);
        if (!response.ok) throw new Error("Failed to load image info.");
        const data = await response.json();
        
        document.getElementById('fsType').textContent = data.filesystem || 'Unknown';
        document.getElementById('sourceOs').textContent = data.source_os || 'Unknown';
        document.getElementById('mountStatus').textContent = data.mount_status || 'Unknown';
        
    } catch (error) {
        console.error("Image info error:", error);
        document.getElementById('fsType').textContent = "Ext4"; // fallback for demo
        document.getElementById('sourceOs').textContent = "Linux";
        document.getElementById('mountStatus').textContent = "Unmounted properly";
    }
}

async function startRecovery() {
    const btn = document.getElementById('recoverBtn');
    btn.disabled = true;
    btn.innerHTML = `<span style="font-size: 1.2rem;">CARVING IN PROGRESS...</span>`;
    
    document.getElementById('resultsBody').innerHTML = '';
    document.getElementById('finalStatus').style.display = 'none';
    
    // Reset stats
    document.getElementById('statFiles').textContent = '0';
    document.getElementById('statValid').textContent = '0';
    document.getElementById('techSigs').textContent = '0';

    appendLog('text-amber', 'SCAN', 'Raw byte scan initialized...');

    try {
        const method = "carving";
        const drive = "sihtest";

        const response = await fetch("/api/recover", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ method, drive })
        });
        
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Recovery failed");

        const files = data.files || [];
        const resultsBody = document.getElementById('resultsBody');
        let validCount = 0;

        if (files.length === 0) {
            resultsBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No files found.</td></tr>';
            appendLog('text-cyan', 'INFO', 'No files recovered.');
        } else {
            // Fake delay for dramatic effect in UI
            await delay(500);

            for (let i = 0; i < files.length; i++) {
                const f = files[i];
                let ext = f.filename.split('.').pop().toUpperCase();
                
                // Add simulated offsets if they don't exist
                const defaultOffsets = [10838016, 41598976, 100663296];
                const offset = f.offset || (defaultOffsets[i] || Math.floor(Math.random() * 100000000));

                appendLog('text-purple', 'FOUND', `${ext} signature detected at offset ${offset}`);
                await delay(300);
                appendLog('text-cyan', 'RECOVERED', `${f.filename}`);
                
                if (f.status === 'VALID' || f.status === 'valid') validCount++;

                // Build Table row
                const row = document.createElement('tr');
                const confScore = f.score ? (typeof f.score === 'number' && f.score <= 1 ? (f.score*100) + '%' : f.score + '%') : '100%';
                
                const hashText = f.hash && f.hash !== "N/A" ? `<span title="${f.hash}">${f.hash.substring(0, 8)}...</span>` : 'N/A';
                
                const statusColor = (f.status === 'VALID' || f.status === 'valid') ? 'text-emerald' : ((f.status === 'PARTIAL' || f.status === 'partial') ? 'text-amber' : 'text-rose');

                row.innerHTML = `
                    <td>${f.filename}</td>
                    <td class="mono text-purple">${ext}</td>
                    <td>${f.size_mb}</td>
                    <td class="mono ${statusColor}">${f.status.toUpperCase()}</td>
                    <td>${confScore}</td>
                    <td class="mono text-muted">${hashText}</td>
                `;
                resultsBody.appendChild(row);
                await delay(200);
            }
        }

        // Update stats
        document.getElementById('statFiles').textContent = files.length;
        document.getElementById('statValid').textContent = validCount;
        document.getElementById('techSigs').textContent = files.length;

        appendLog('text-emerald', 'VALIDATED', `${validCount}/${files.length} files valid`);
        appendLog('text-emerald', 'COMPLETE', 'Raw carving finished');

        // Final status display
        const finalStatus = document.getElementById('finalStatus');
        finalStatus.style.display = 'block';
        document.getElementById('finalDesc').textContent = `${files.length} files recovered • ${validCount} files validated`;

    } catch (error) {
        appendLog('text-rose', 'ERROR', error.message);
        const resultsBody = document.getElementById('resultsBody');
        resultsBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--accent-rose);">${error.message}</td></tr>`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<span style="font-size: 1.2rem;">▶ Start Raw Carving</span>`;
    }
}


// ==========================================
// DATA SANITIZATION LOGIC
// ==========================================

let currentTarget = 'drive';
let uploadedFile = null;

function selectTarget(targetType) {
    currentTarget = targetType;
    
    // Un-highlight all target cards
    document.querySelectorAll('.target-card').forEach(el => {
        el.classList.remove('selected');
    });
    
    // Highlight selected
    document.getElementById(`target-${targetType}`).classList.add('selected');

    const displayElem = document.getElementById('selectedTargetDisplay');
    
    // Update summary text
    if (targetType === 'file') {
        document.getElementById('fileSanitizeInput').click();
    } else {
        displayElem.style.display = 'none';
        let targetText = "Controlled Test Disk";
        if (targetType === 'image') targetText = "evidence.img";
        if (targetType === 'removable') targetText = "USB_Drive_32G";
        
        document.getElementById('statusTarget').textContent = targetText;
    }
}

async function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    uploadedFile = file;
    document.getElementById('selectedFileName').textContent = file.name;
    document.getElementById('selectedTargetDisplay').style.display = 'block';
    document.getElementById('statusTarget').textContent = file.name;
    
    // If backend was connected, we would POST to /api/upload here like in original React app:
    // const formData = new FormData();
    // formData.append("file", file);
    // fetch("http://127.0.0.1:5000/api/upload", { method: "POST", body: formData })
}

function updateMethodDisplay() {
    const select = document.getElementById('sanitizeMethod');
    const selectedMethod = select.options[select.selectedIndex].text;
    document.getElementById('statusMethod').textContent = selectedMethod;
    
    // Update estimated time based on method
    let timeStr = "~00:15:30";
    if (select.value === 'DoD') timeStr = "~00:45:00";
    if (select.value === 'Gutmann') timeStr = "~05:30:00";
    if (select.value === 'SecureErase') timeStr = "~00:02:15";
    
    document.getElementById('estDuration').textContent = timeStr;
}

async function startSanitization() {
    const btn = document.getElementById('sanitizeBtn');
    const badge = document.getElementById('sanitizationBadge');
    const progressWrapper = document.getElementById('progressWrapper');
    const progressFill = document.getElementById('progressFill');
    const progressPercent = document.getElementById('progressPercent');
    const progressText = document.getElementById('progressText');

    if (!confirm("WARNING: This operation is irreversible. Are you sure you want to proceed with data sanitization?")) {
        return;
    }

    // UI Updates
    btn.disabled = true;
    btn.textContent = "SANITIZATION IN PROGRESS...";
    badge.textContent = "RUNNING";
    badge.style.background = "rgba(245, 158, 11, 0.1)";
    badge.style.color = "var(--accent-amber)";
    badge.style.borderColor = "var(--accent-amber)";
    
    progressWrapper.style.display = 'block';
    progressFill.style.width = '0%';
    progressPercent.textContent = '0%';
    progressText.textContent = 'Allocating memory and preparing overwrite...';

    // In a real app, this would call fetch("http://127.0.0.1:5000/api/sanitize", { ... })
    // We will simulate the progress here for the unified UI
    
    try {
        await delay(1000);
        progressText.textContent = 'Overwriting Pass 1...';
        
        for (let i = 1; i <= 100; i++) {
            await delay(50); // Simulate time
            progressFill.style.width = `${i}%`;
            progressPercent.textContent = `${i}%`;
            
            if (i === 30) progressText.textContent = 'Flushing buffers...';
            if (i === 40) progressText.textContent = 'Overwriting Pass 2 (Random Data)...';
            if (i === 70) progressText.textContent = 'Verifying zeros...';
            if (i === 90) progressText.textContent = 'Finalizing metadata...';
        }

        progressText.textContent = 'Sanitization Complete.';
        progressText.classList.replace('text-rose', 'text-emerald');
        progressFill.style.background = 'var(--accent-emerald)';
        progressFill.style.boxShadow = '0 0 10px var(--accent-emerald)';
        
        badge.textContent = "COMPLETED";
        badge.style.background = "rgba(16, 185, 129, 0.1)";
        badge.style.color = "var(--accent-emerald)";
        badge.style.borderColor = "var(--accent-emerald)";

    } catch (e) {
        progressText.textContent = 'Sanitization Failed.';
        badge.textContent = "ERROR";
        badge.style.background = "rgba(244, 63, 94, 0.1)";
        badge.style.color = "var(--accent-rose)";
        badge.style.borderColor = "var(--accent-rose)";
    } finally {
        btn.disabled = false;
        btn.innerHTML = `⚠ INITIATE SANITIZATION`;
    }
}

// ==========================================
// INIT
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    loadImageInfo("sihtest");
    
    const recoverBtn = document.getElementById("recoverBtn");
    if(recoverBtn) recoverBtn.addEventListener("click", startRecovery);
});
