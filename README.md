# Forensic Core
### Integrated Secure Data Erasure & Advanced File Recovery Tool for Digital Forensics and Data Sanitization

**Smart India Hackathon 2026**
**Problem Statement ID:** 26149
**Theme:** Blockchain & Cybersecurity
**PS Category:** Software
**Team Name:** Gigabyte

---

## 1. Problem We Are Solving

Organizations, government agencies, law enforcement units, and individuals face two disconnected challenges:

1. **Securely destroying sensitive data** so it cannot be recovered after disposal or reuse of storage media.
2. **Recovering deleted digital evidence** during forensic investigations, often from formatted, damaged, or corrupted media.

Existing tools solve only one side of this problem at a time, forcing investigators to juggle multiple disconnected tools, increasing cost, complexity, and the chance of procedural error. There is no widely available platform that treats sanitization and recovery as **two halves of the same evidentiary process.**

## 2. Our Core Idea

> **Don't just erase data. Prove what was recoverable before sanitization — and prove what remains afterward.**

Forensic Core is a unified platform that closes the loop between destruction and recovery:

```
RECOVER → MEASURE → BASELINE → SANITIZE → RECOVER AGAIN → COMPARE → VERIFY → REPORT
```

Instead of treating "erase" and "recover" as separate tools with separate outputs, our platform uses recovery *as the verification mechanism* for sanitization — producing a certificate that proves, with forensic evidence, that a wipe actually worked.

## 3. Alignment with the Problem Statement

| PS Requirement | Our Solution |
|---|---|
| Secure Drive Eraser (HDD/SSD/USB/memory cards) | Media classification engine identifies drive type and recommends a sanitization method per class (see §7, MVP Scope) |
| Secure File & Folder Eraser with metadata cleansing | File/Folder Sanitization module — target identification, SHA-256 capture, sanitization, status + timestamp logging |
| Advanced File Carving & Recovery (signature-based, structure-based, intelligent) | Sleuth Kit filesystem recovery + raw signature-based carving + structural/parser validation, fused into an explainable confidence score |
| Recovery without filesystem metadata | Raw file carving pipeline operates directly on disk-image bytes independent of filesystem metadata |
| Fragmented file reconstruction | Reconstruction module using structural markers and block/cluster evidence |
| Automatic classification & confidence scoring | Explainable Recovery Confidence: signature validity + structural validity + parser validation + filesystem evidence + integrity, combined into a weighted score |
| Comprehensive audit logs & tamper-resistant reporting | Hash-chained tamper-evident audit trail, with periodic on-chain anchoring (see §5) |
| Compliance with data destruction standards | Sanitization method recommendations are modeled on **NIST SP 800-88 (Clear / Purge / Destroy)** categorization |
| User-friendly GUI | Unified dashboard covering Evidence, Recovery, Sanitization, Verification, Audit, and Reports in one interface |

## 4. What Makes This Different (USP)

1. **Sanitization proven by evidence, not just claimed.** We run recovery before and after sanitization and compare results — the certificate we generate states plainly whether previously identified artifacts are still recoverable.
2. **Explainable confidence, not a black-box score.** Every recovered file's confidence score is broken down into the individual checks that produced it (signature, structure, parser, filesystem evidence, integrity) — auditable by a human reviewer, not just a number.
3. **One platform instead of three tools.** Sanitization, recovery, and verification share one evidence model, one audit trail, and one reporting pipeline.
4. **Tamper-evident audit trail anchored to blockchain.** Our hash-chained audit log periodically anchors its latest hash to a public/testnet blockchain, so audit integrity can be independently verified even outside our own system — directly addressing the hackathon's Blockchain & Cybersecurity theme.
5. **Verification is a testable, falsifiable claim, not a UI badge.** Before/after comparison is implemented as its own module with a strict PASS/FAIL contract based on artifact overlap — not a cosmetic "success" message. We treat "prove it's wiped" as fundamentally different from "say it's wiped."
6. **Chain-of-custody, not just audit logging.** Our tamper-evident trail is framed and structured around chain-of-custody principles consistent with forensic standards such as ISO/IEC 27037 — positioning the platform as producing evidence suitable for investigative and legal use, not just an internal activity log.
7. **Honest negative-result reporting.** The system reports what it could *not* recover, and why — e.g., an artifact with a valid signature but failed parser validation is explicitly classified INVALID rather than silently dropped. Forensic tools that surface their own failure cases are inherently more trustworthy than ones that only report successes.
8. **Independently reproducible verification.** Because every recovery artifact, sanitization result, and audit event is captured as structured JSON, the entire verification procedure can be re-run and independently confirmed by a third party from the exported evidence — not just trusted from a generated PDF certificate.

## 5. Blockchain Usage

Our audit trail is a hash-chained log (each event's hash depends on the previous event's hash, so any retroactive edit breaks the chain). To make this tamper-evidence independently verifiable — not just self-reported — we anchor the latest chain hash and/or final sanitization certificate hash to a blockchain testnet (e.g., Polygon Amoy) via a lightweight smart contract. This means the authenticity of a sanitization certificate can be checked by a third party on a public block explorer, independent of trusting our own servers.

## 6. System Architecture

```
                     USER / INVESTIGATOR
                            │
                            ▼
                      UNIFIED GUI
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   SANITIZATION       FILE RECOVERY      INTELLIGENCE &
   & FILE ERASE       & FILE CARVING      VERIFICATION
        │                   │                   │
        ▼                   ▼                   ▼
  File / Folder /     Sleuth Kit +        Confidence Scoring
  Disk-Image Wipe     Raw Carving +       Baseline / Compare
  Media Classifier    Reconstruction      Audit Trail (chain +
                       + Validation        blockchain anchor)
        │                   │                   │
        └───────────────────┴───────────────────┘
                            ▼
                 CONSOLIDATED REPORT +
                 SANITIZATION CERTIFICATE
```

## 7. Current MVP Scope (Hackathon Build)

Built within a focused development window on **controlled test disk images**, to demonstrate the full evidentiary loop safely:

**Sanitization**
- File, folder, and controlled disk-image sanitization
- Storage-media classification (HDD / SSD / USB / Disk Image / Unknown)
- NIST 800-88–aligned method recommendation
- Safety layer: explicit confirmation, target path + SHA-256 display before any destructive action

**Recovery**
- Sleuth Kit integration (`mmls`, `fsstat`, `fls`, `istat`) for filesystem-based recovery
- Raw signature-based file carving for JPEG, PNG, PDF, DOCX, ZIP
- Fragmented file reconstruction (best-effort, structure-evidence based)
- File validation: signature check, structural check, parser validation, integrity check

**Intelligence & Verification**
- Explainable recovery confidence score
- Aggregate recoverability score
- Pre/post-sanitization baseline comparison
- PASS/FAIL sanitization verification
- Hash-chained, blockchain-anchored audit trail
- Automated forensic report and sanitization certificate generation

### Honest Scope Boundaries (stated upfront, not discovered)

We deliberately scope the hackathon MVP for safety, reliability, and time:

- **Physical drive wiping is not performed automatically in this MVP.** For HDD/SSD/USB targets, the system demonstrates media classification and method recommendation rather than executing destructive wipes on real physical devices — SSD/NVMe wear-leveling in particular makes "permanent deletion" claims unreliable without specialized ATA Secure Erase support, which is flagged as a planned enhancement.
- **Current backend drive-detection is Windows-first** (PowerShell `Get-Disk`/`Get-Volume`). Cross-platform support (Linux `lsblk`, macOS `diskutil`) is a near-term roadmap item; file/folder/disk-image sanitization and recovery themselves are OS-independent.
- **AI/ML-based classification is intentionally excluded from the MVP** in favor of deterministic, explainable checks (signature/structure/parser/filesystem evidence). This is a stronger fit for forensic admissibility than an unexplained model score, and AI-assisted prioritization is listed as a future enhancement, not a gap we're hiding.

## 8. Recovery Confidence Model

Each recovered artifact is scored using a transparent, evidence-weighted formula:

| Check | Weight |
|---|---|
| Valid file signature | 30% |
| Valid internal structure | 25% |
| Parser validation passed | 25% |
| Filesystem evidence present | 20% |

**Recoverability Score** = average confidence score across all currently-recoverable artifacts in a given scan.

**Verification Logic:** Sanitization is marked **PASS** only if the set of artifacts recoverable after sanitization has zero overlap (by SHA-256 / filename+offset) with the pre-sanitization baseline. Any overlap results in **FAIL**.

## 9. Sample Output — Sanitization Certificate

```
==================================================
          SANITIZATION CERTIFICATE
==================================================
Target              : carving.img
SHA-256              : <hash>

PRE-SANITIZATION
Artifacts Recovered : 5
Recovery Confidence : <score>
Recoverability      : <score>

SANITIZATION
Method              : <NIST 800-88 aligned method>
Status              : COMPLETED

POST-SANITIZATION
Artifacts Recovered : 0

VERIFICATION         : PASS
AUDIT INTEGRITY       : VALID (chain-verified + blockchain-anchored)

Statement:
No previously identified artifacts were recovered
under the defined verification procedure.
==================================================
```

## 10. Impact

- **Reduces tool fragmentation** — one platform instead of separate erasure and recovery tools.
- **Improves auditability** — every sanitization claim is backed by a verifiable, tamper-evident record.
- **Supports safe data lifecycle management** — organizations can prove data was destroyed before reuse or disposal of storage.
- **Speeds up forensic investigations** — combined filesystem + carving recovery increases artifact recovery rate from a single pass.

## 11. Technology Stack

| Layer | Technology |
|---|---|
| Digital Forensics | The Sleuth Kit (`mmls`, `fsstat`, `fls`, `istat`) |
| File Recovery | Signature/magic-byte scanning, structural parsing, raw carving |
| Security | SHA-256, hash-chained audit log, blockchain anchoring (testnet) |
| Backend | Python, FastAPI |
| Frontend | React (Vite) |
| OS (current build) | Windows (PowerShell-based drive detection); cross-platform planned |

## 12. Research & References

1. *Forensic Science International: Digital Investigation* (2023) — Identification of data wiping tools based on deletion patterns in ReFS `$Logfile`.
2. *arXiv* (2026) — Byte-level generative predictions for forensic multimedia carving.
3. *CUSTOS* — Toward Forensic-Ready Zero Trust at the Capture-Containment Boundary.
4. The Sleuth Kit (TSK) — official documentation and developer guide.
5. NIST Special Publication 800-88 Rev. 1 — Guidelines for Media Sanitization.

## 13. Future Enhancements

- Cross-platform drive detection and physical-device sanitization (with ATA Secure Erase / NVMe Format support)
- Additional filesystem and file-format support
- AI/ML-assisted artifact classification and recovery prioritization
- Parallel carving for large disk images
- Multi-user investigator workflows and case management
- Enterprise-scale reporting and cloud-based investigation support

---

# Developer Setup Guide

## Project Structure

```
├── app/                      # FastAPI backend
└── SIH-GUI/secureerase-sih/  # React (Vite) frontend
```

## Prerequisites

- Node.js v16+ and npm
- Python 3.8+
- Windows OS with PowerShell (current backend uses `Get-Disk` / `Get-Volume` for drive scanning)
- Administrator privileges (required for raw drive recovery endpoints)

## Backend Setup

```bash
# From the repository root
python -m venv venv
venv\Scripts\activate

pip install fastapi uvicorn pydantic python-multipart

# Run the backend (from repo root, since app/ is a module)
uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

## Frontend Setup

```bash
cd SIH-GUI/secureerase-sih
npm install
npm run dev
```

- App: `http://localhost:5173`

## How It Works

- The React frontend (`5173`) calls the FastAPI backend (`8000`); CORS is currently open (`*`) for development.
- `/api/drives` uses `subprocess.run` to call PowerShell (`Get-Disk`, `Get-Volume`) for drive detection.
- `/api/upload` saves uploaded disk images to a local `data/` folder (created automatically).
- `/api/recover` delegates to `RecoveryEngine` in `app.recovery`.

## Troubleshooting

- **PowerShell commands failing:** Run the backend as Administrator and ensure PowerShell script execution is permitted.
- **Port already in use:**
  - Backend: `uvicorn app.main:app --reload --port 8080`
  - Frontend: `npm run dev -- --port 3000`

---

*Developed for Smart India Hackathon 2026 — Problem Statement 26149 — Team Gigabyte.*