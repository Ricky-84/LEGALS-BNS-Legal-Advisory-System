# LEGALS: Legal Empowerment and Awareness System

A deterministic legal AI system to facilitate citizen's legal empowerment and awareness by mapping users' natural language descriptions to relevant Indian laws (Bharatiya Nyaya Sanhita - BNS).

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Legal Disclaimer](#legal-disclaimer)

---

## Overview

LEGALS is an academic project demonstrating how AI and graph databases can be used for legal technology. The system:
- Accepts natural language legal queries (English/Hindi)
- Extracts entities using Phi-3 AI model
- Maps queries to relevant BNS (Bharatiya Nyaya Sanhita) sections using Neo4j knowledge graph
- Provides citizen-friendly legal guidance with applicable laws and punishments

---

## Key Features

- **Deterministic Legal Reasoning**: Uses Neo4j graph database for rule-based legal classification
- **Entity Extraction**: Phi-3-mini model extracts factual entities without legal interpretation
- **Multilingual Support**: English and Hindi language processing (when Azure Translator is configured)
- **Voice Input**: Speech-to-text capability (when Google Speech is configured)
- **Real-time Processing**: WebSocket-based communication
- **Property Value Analysis**: Estimates stolen property value for punishment determination
- **Fact Verification**: Cross-validation against legal knowledge base

**Currently Supported Offences:**
- Theft (BNS-303)
- Snatching (BNS-304)
- Theft in dwelling house (BNS-305)
- Theft by employee (BNS-306)
- Extortion (BNS-308)
- Robbery (BNS-309)
- Criminal breach of trust (BNS-316)
- Cheating (BNS-318)
- Mischief (BNS-324)
- Criminal trespass (BNS-329)

---

## Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **Frontend**: React 18, Material UI
- **Databases**:
  - Neo4j Community Edition (primary - for legal knowledge graph)
  - PostgreSQL (optional - for user session management)
- **AI Model**: Phi-3-latest (via Ollama)
- **External Services** (Optional):
  - Azure Translator (multilingual support)
  - Google Speech V2 (voice input)

---

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Python 3.11 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Node.js 16+ and npm**
   - Download from: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **Neo4j Desktop**
   - Download from: https://neo4j.com/download/
   - This is the primary database for legal reasoning

4. **Ollama** (for AI model)
   - Download from: https://ollama.com/download
   - Verify: `ollama --version`

### Optional Software

5. **PostgreSQL** (optional - for user management)
   - Download from: https://www.postgresql.org/download/
   - Can be skipped for basic functionality

6. **Git** (to clone the repository)
   - Download from: https://git-scm.com/downloads

---

## Installation Guide

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd LEGALS-BNS-Legal-Advisory-System-main
```

### Step 2: Python Environment Setup

#### Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (use Windows-compatible version)
pip install --upgrade pip
pip install -r requirements_windows.txt
```

#### Linux/Mac:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Note for Windows users:** If you encounter build errors with `psycopg2-binary` or `numpy`, use `requirements_windows.txt` which has version constraints to avoid compilation issues.

### Step 3: Frontend Setup

```bash
cd frontend
npm install
cd ..
```

**Note:** You may see some npm audit warnings - these are for development dependencies and can be safely ignored for local development.

### Step 4: Ollama Model Setup

```bash
# Pull the Phi-3 model (this will download ~2.2GB)
ollama pull phi3:latest

# Verify the model is available
ollama list
```

You should see `phi3:latest` in the list of models.

---

## Database Setup

### Neo4j Setup (Required)

Neo4j is the primary database that stores the BNS legal knowledge graph.

#### 1. Install and Start Neo4j Desktop

1. Open **Neo4j Desktop**
2. Create a new project (or use existing)
3. Click **"Add"** → **"Local DBMS"**
4. Set:
   - Name: `legalknowledge` (or any name you prefer)
   - Password: Choose a secure password (you'll need this later)
   - Version: Use latest available (5.x recommended)
5. Click **"Create"**
6. **Start** the database

#### 2. Create the Database

1. Click on your DBMS in Neo4j Desktop
2. Click **"Open with Neo4j Browser"** (or go to http://localhost:7474)
3. Login with username `neo4j` and the password you set
4. In the query box, run:

```cypher
CREATE DATABASE legalknowledge
```

5. Switch to this database:

```cypher
:use legalknowledge
```

#### 3. Import Legal Data

The BNS legal data is stored in CSV format and needs to be imported into Neo4j.

**A. Locate the Neo4j Import Folder:**

1. In Neo4j Desktop, click the **three dots (...)** next to your database
2. Select **"Open Folder"** → **"Import"**
3. This opens the import directory in your file explorer

**B. Copy the CSV File:**

Copy this file from your project to the Neo4j import folder:
```
data/csv_friend/bns_ch17_final_cleaned.csv
```

**C. Run the Import Query:**

In Neo4j Browser (http://localhost:7474), ensure you're using the `legalknowledge` database.

**Option 1: Use the provided Cypher file (Recommended)**

Open `neo4j_import.cypher` from the project root. This file contains all import and verification queries with detailed comments. Copy and run the queries step-by-step.

**Option 2: Manual query**

Run this query directly:

```cypher
LOAD CSV WITH HEADERS FROM 'file:///bns_ch17_final_cleaned.csv' AS row
WITH row
WHERE row.s_section_number IS NOT NULL AND trim(row.s_section_number) <> ""

// Create Chapter node
MERGE (c:Chapter {
    number: "XVII",
    title: "Of Offences Against Property"
})

// Create Section nodes
MERGE (s:Section {
    section_id: "BNS-" + row.s_section_number,
    section_number: toInteger(row.s_section_number),
    title: row.s_section_title,
    text: row.s_section_text
})

// Create Offence nodes with proper type mapping
MERGE (o:Offence {
    section_id: "BNS-" + row.s_section_number,
    type: CASE toInteger(row.s_section_number)
        WHEN 303 THEN 'theft'
        WHEN 304 THEN 'snatching'
        WHEN 305 THEN 'dwelling_theft'
        WHEN 306 THEN 'employee_theft'
        WHEN 307 THEN 'prepared_theft'
        WHEN 308 THEN 'extortion'
        WHEN 309 THEN 'robbery'
        WHEN 310 THEN 'dacoity'
        WHEN 311 THEN 'armed_robbery'
        WHEN 316 THEN 'breach_of_trust'
        WHEN 318 THEN 'cheating'
        WHEN 324 THEN 'mischief'
        WHEN 329 THEN 'criminal_trespass'
        ELSE 'other'
    END,
    section_number: toInteger(row.s_section_number)
})

// Create Punishment nodes
MERGE (p:Punishment {
    punishment_id: 'PUN_' + row.s_section_number,
    section_id: "BNS-" + row.s_section_number,
    description: row.punishment,
    punishment_type: 'imprisonment_and_fine'
})

// Create relationships
MERGE (c)-[:CONTAINS]->(s)
MERGE (s)-[:DEFINES]->(o)

RETURN
    count(DISTINCT c) as chapters_created,
    count(DISTINCT s) as sections_created,
    count(DISTINCT o) as offences_created,
    count(DISTINCT p) as punishments_created
```

**D. Verify the Import:**

Run this query to verify the data was imported correctly:

```cypher
MATCH (s:Section)-[:DEFINES]->(o:Offence)
MATCH (p:Punishment)
WHERE s.section_number = 303 AND p.section_id = s.section_id
RETURN s.section_id, s.title, o.type, p.description
LIMIT 1
```

You should see data for Section 303 (Theft).

**Expected Results:**
- Chapters: 1
- Sections: 32
- Offences: 32
- Punishments: 32

### PostgreSQL Setup (Optional)

PostgreSQL is used for user session management but is **not required** for core legal reasoning functionality. You can skip this if you just want to test the system.

If you want to set it up:

1. Install PostgreSQL from https://www.postgresql.org/download/
2. Create a database named `legals_db`
3. Note your postgres username and password for configuration

---

## Configuration

### Backend Configuration

1. Navigate to the `backend/` directory
2. Create a `.env` file (copy from `.env.example` if available):

```bash
cd backend
# Create .env file
```

3. Add the following configuration to `backend/.env`:

```env
# Database Configuration (PostgreSQL - optional)
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=legals_db

# Neo4j Configuration (Required)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password

# Ollama Configuration (Required)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:latest

# External Services (Optional - leave empty if not using)
AZURE_TRANSLATOR_KEY=
AZURE_TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com
AZURE_TRANSLATOR_REGION=

GOOGLE_SPEECH_CREDENTIALS=

# Security
SECRET_KEY=your-super-secret-key-change-in-production
```

**Important:** Replace the following values:
- `your_neo4j_password` - The password you set when creating the Neo4j database
- `your_postgres_password` - Your PostgreSQL password (if using PostgreSQL)
- `your-super-secret-key-change-in-production` - A random secret key

### Frontend Configuration

The frontend is already configured to proxy API requests to `http://localhost:8000` (see `frontend/package.json`). No additional configuration needed.

---

## Running the Application

### Step 1: Start Neo4j Database

Make sure your Neo4j database is running in Neo4j Desktop.

### Step 2: Start Ollama Service

Ollama should start automatically when you installed it. Verify it's running:

```bash
ollama list
```

### Step 3: Start Backend Server

Open a terminal/command prompt:

```bash
# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Navigate to backend directory
cd backend

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

**Backend is now running at:**
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Step 4: Start Frontend Server

Open a **NEW** terminal/command prompt (keep backend running):

```bash
# Navigate to frontend directory
cd frontend

# Start React development server
npm start
```

The browser should automatically open to http://localhost:3000

**If it doesn't open automatically, manually navigate to:**
- Frontend: http://localhost:3000

---

## Testing

### Quick Manual Test

1. Open the frontend at http://localhost:3000
2. Enter a test query like:
   - "Someone stole my iPhone from my house"
   - "My employee took cash from the office"
   - "A robber threatened me with a knife and took my wallet"
3. Click submit and verify you get applicable BNS sections

### Automated Tests

Run the test suite to verify all components:

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Test Neo4j connection and legal reasoning
python backend/test_neo4j_only.py

# Test Ollama AI model integration
python backend/test_ollama.py

# Test complete pipeline (Neo4j + Ollama)
python backend/test_complete_pipeline.py
```

**Expected Results:**
- `test_neo4j_only.py`: 4/4 tests passed
- `test_ollama.py`: 4/5 tests passed (one test may fail due to model variations)
- `test_complete_pipeline.py`: 5/5 tests passed

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Python Package Installation Errors (Windows)

**Problem:**
```
ERROR: Failed to build 'psycopg2-binary' when getting requirements to build wheel
```

**Solution:**
Use `requirements_windows.txt` instead of `requirements.txt`:
```bash
pip install -r requirements_windows.txt
```

This file uses version constraints (>=) instead of exact versions (==) to allow pip to find prebuilt wheels.

---

#### 2. Neo4j Connection Failed

**Problem:**
```
Neo4j connection failed: The client is unauthorized due to authentication failure
```

**Solution:**
- Verify Neo4j Desktop is running
- Check the password in `backend/.env` matches your Neo4j password
- Ensure you're using the correct database name (`legalknowledge`)

---

#### 3. Neo4j Database Empty / No Laws Found

**Problem:**
Tests pass but return 0 applicable laws.

**Solution:**
You imported data into the wrong database. Make sure to:

1. In Neo4j Browser, run: `:use legalknowledge`
2. Verify with: `MATCH (s:Section) RETURN count(s)`
3. If count is 0, re-run the CSV import query (see Database Setup section)

---

#### 4. Ollama Model Not Found

**Problem:**
```
ERROR: Phi-3 model request failed with status 404
```

**Solution:**
```bash
# Pull the model
ollama pull phi3:latest

# Verify it's available
ollama list
```

Make sure `OLLAMA_MODEL=phi3:latest` in your `.env` file.

---

#### 5. CSV Import Error in Neo4j

**Problem:**
```
Couldn't load the external resource at: file:///bns_ch17_final_cleaned.csv
```

**Solution:**
- The CSV file must be in Neo4j's import directory
- In Neo4j Desktop: Click database → Three dots → Open Folder → Import
- Copy `data/csv_friend/bns_ch17_final_cleaned.csv` to this directory
- Make sure you're using `:use legalknowledge` before running the import

---

#### 6. Frontend Not Connecting to Backend

**Problem:**
Frontend shows connection errors or "Cannot reach server"

**Solution:**
- Verify backend is running at http://localhost:8000
- Check `frontend/package.json` has `"proxy": "http://localhost:8000"`
- Clear browser cache and restart frontend: `npm start`

---

#### 7. Port Already in Use

**Problem:**
```
ERROR: Address already in use (Port 8000 or 3000)
```

**Solution:**

**Windows:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or for port 3000
lsof -ti:3000 | xargs kill -9
```

---

#### 8. Virtual Environment Issues

**Problem:**
Packages not found or import errors

**Solution:**
Make sure virtual environment is activated:

**Windows:**
```bash
# You should see (venv) in your command prompt
venv\Scripts\activate
```

**Linux/Mac:**
```bash
# You should see (venv) in your terminal
source venv/bin/activate
```

If packages are still missing:
```bash
pip install -r requirements_windows.txt  # Windows
# or
pip install -r requirements.txt  # Linux/Mac
```

---

#### 9. npm Install Vulnerabilities

**Problem:**
```
9 vulnerabilities (3 moderate, 6 high)
```

**Solution:**
These are in development dependencies and can be safely ignored for local development. Do NOT run `npm audit fix --force` as it may break react-scripts.

---

#### 10. Neo4j Browser Authentication Loop

**Problem:**
Keep getting asked to login in Neo4j Browser

**Solution:**
1. Disconnect from the current connection
2. Connect with:
   - URL: `neo4j://localhost:7687` or `bolt://localhost:7687`
   - Username: `neo4j`
   - Password: Your database password
   - Database: `legalknowledge`

---

### Still Having Issues?

1. **Check all services are running:**
   - Neo4j Desktop → Database is started (green play button)
   - Ollama: `ollama list` shows phi3:latest
   - Backend: http://localhost:8000/docs is accessible
   - Frontend: http://localhost:3000 loads

2. **Check logs:**
   - Backend logs in the terminal where you ran uvicorn
   - Frontend logs in browser console (F12)
   - Neo4j logs in Neo4j Desktop → Database → Three dots → Logs

3. **Restart everything:**
   ```bash
   # Stop all servers (Ctrl+C in terminals)
   # Restart Neo4j Desktop database
   # Restart Ollama if needed: ollama serve
   # Restart backend: uvicorn main:app --reload
   # Restart frontend: npm start
   ```

---

## Project Structure

```
LEGALS-BNS-Legal-Advisory-System-main/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── core/              # Core configurations
│   │   │   └── config.py      # Settings and environment variables
│   │   ├── services/          # Business logic
│   │   │   ├── neo4j_service.py          # Neo4j legal reasoning
│   │   │   ├── ollama_service.py         # AI entity extraction
│   │   │   ├── legal_processing_service.py
│   │   │   └── property_value_estimator.py
│   │   ├── routers/           # API endpoints
│   │   └── models/            # Data models
│   ├── main.py                # FastAPI application entry point
│   ├── .env                   # Environment configuration (create this)
│   ├── .env.example           # Example configuration
│   └── test_*.py              # Test files
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API services
│   │   └── App.js             # Main application
│   ├── public/
│   ├── package.json
│   └── package-lock.json
│
├── data/
│   ├── csv_friend/
│   │   └── bns_ch17_final_cleaned.csv    # BNS legal data (for Neo4j import)
│   ├── csv_exports/           # Exported CSV files
│   └── bns_data/              # Original BNS data
│
├── requirements.txt           # Python dependencies (Linux/Mac)
├── requirements_windows.txt   # Python dependencies (Windows)
├── README.md                  # This file
└── tasks/
    └── todo.md               # Setup completion log
```

---

## Architecture

### System Flow

```
User Query (Natural Language)
       ↓
Frontend (React + Material UI)
       ↓
Backend API (FastAPI)
       ↓
    ┌──────────────────────────┐
    │  Entity Extraction       │
    │  (Ollama + Phi-3-mini)   │ → Extracts: persons, objects, locations, actions, etc.
    └──────────────────────────┘
       ↓
    ┌──────────────────────────┐
    │  Legal Reasoning         │
    │  (Neo4j Knowledge Graph) │ → Matches entities to BNS sections
    └──────────────────────────┘
       ↓
    ┌──────────────────────────┐
    │  Property Value Analysis │ → Estimates stolen property value
    └──────────────────────────┘
       ↓
Legal Analysis Result (Applicable laws + Punishments + Confidence scores)
```

### Database Schema (Neo4j)

```
(Chapter)-[:CONTAINS]->(Section)-[:DEFINES]->(Offence)
                           ↓
                      (Punishment)
                    [linked by section_id]
```

**Node Types:**

1. **Chapter**: Contains metadata about BNS chapters
   - Properties: `number`, `title`

2. **Section**: Legal sections from BNS
   - Properties: `section_id`, `section_number`, `title`, `text`

3. **Offence**: Types of offences defined by sections
   - Properties: `offence_id`, `type`, `section_number`
   - Types: `theft`, `snatching`, `robbery`, `extortion`, etc.

4. **Punishment**: Punishment details for each section
   - Properties: `punishment_id`, `section_id`, `description`, `punishment_type`

### API Endpoints

**Main Endpoint:**
- `POST /api/v1/legal/query` - Submit legal query and get analysis

**Documentation:**
- `GET /docs` - Swagger UI API documentation
- `GET /redoc` - ReDoc API documentation

---

## Performance Notes

- **Entity Extraction**: ~2-3 seconds per query (depends on Ollama/hardware)
- **Legal Reasoning**: <1 second (Neo4j graph queries are fast)
- **Property Value Estimation**: <1 second
- **End-to-End Query**: ~3-5 seconds total

**Optimization Tips:**
- Use SSD for Neo4j database storage
- Allocate sufficient RAM to Neo4j (4GB+ recommended)
- Ollama performance depends on CPU/GPU - GPU acceleration significantly faster

---

## Development Notes

### Adding New BNS Sections

To add more BNS chapters/sections:

1. Prepare CSV file with same structure as `bns_ch17_final_cleaned.csv`
2. Place in Neo4j import folder
3. Update the import Cypher query with new offence type mappings
4. Update `neo4j_service.py` to add detection logic for new offence types

### Running in Production

**Security Checklist:**
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Use strong passwords for Neo4j and PostgreSQL
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly in `backend/app/core/config.py`
- [ ] Set up authentication/authorization
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging

---

## Legal Disclaimer

⚖️ **IMPORTANT LEGAL NOTICE** ⚖️

This system provides **preliminary legal information only** and is **NOT a replacement for qualified legal counsel**.

**Limitations:**
- This is an academic/demonstration project
- Legal advice requires professional judgment and case-specific analysis
- AI systems can make errors or provide incomplete information
- Indian law is complex and constantly evolving
- This system covers only a limited subset of BNS (Chapter XVII - Offences Against Property)

**Users must:**
- Consult qualified lawyers for actionable legal advice
- Verify all information independently
- Not rely solely on this system for legal decisions
- Understand this is a research/educational tool

**By using this system, you acknowledge that:**
- You will not use it as a substitute for professional legal counsel
- The developers are not liable for any decisions made based on system output
- You understand the limitations and experimental nature of this project

---

## Contributing

This is an academic project. If you find bugs or have suggestions:

1. Open an issue describing the problem
2. Provide steps to reproduce
3. Include error messages and logs
4. Suggest potential solutions

---

## Development Status

✅ **Core Features Working:**
- Entity extraction (Phi-3-mini via Ollama)
- Legal reasoning (Neo4j graph queries)
- Property value estimation
- Frontend-backend integration
- BNS Chapter XVII (32 sections) support

🚧 **Future Enhancements:**
- Additional BNS chapters
- PostgreSQL user authentication
- Multilingual support (Azure Translator)
- Voice input (Google Speech)
- Case law references
- Legal document generation

---

## License

Academic/Educational Project - Check with repository owner for licensing terms.

---

## Acknowledgments

- **BNS Data**: Bharatiya Nyaya Sanhita (Indian Penal Code replacement)
- **AI Model**: Microsoft Phi-3-mini
- **Technologies**: Neo4j, FastAPI, React, Ollama

---

## Contact & Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the [Troubleshooting](#troubleshooting) section
- Review test files for examples

---

**Last Updated:** November 2024
**Version:** 2.0.0
**Status:** ✅ Fully Functional
