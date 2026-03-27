# IITB Sports Certificate Generation

## Overview

FastAPI backend for generating sports certificates as PDFs from JSON data using Pillow image manipulation.

## Setup

### Prerequisites

- Python 3.7 or higher installed on your system

### Step 1: Clone/Navigate to Project

```bash
cd path/to/IITB\ Sports\ Certificate\ Generation
```

### Step 2: Create Python Virtual Environment

```bash
# On Windows (PowerShell)
python -m venv venv

# On macOS/Linux
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

```bash
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
venv\Scripts\activate.bat

# On macOS/Linux
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal after activation.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- FastAPI
- Uvicorn
- Pillow
- ReportLab
- Jinja2
- Python-multipart

## Run server

### Option A: Using Command Line (Recommended for Quick Generation)

**Generate certificates directly without starting a server:**

```bash
python generate.py
```

**Clear all certificates:**

```bash
python generate.py --clear
```

**Clear and regenerate in one command:**

```bash
python generate.py --clear-gen
```

**View help:**

```bash
python generate.py --help
```

### Option B: Using FastAPI Server

If you need to use the API endpoints (e.g., for frontend integration):

#### Step 5: Start the FastAPI Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

The API is now running on `http://localhost:8000`

#### Step 6: Stop the Server

Press `Ctrl+C` in the terminal to stop the server.

#### Step 7: Deactivate Virtual Environment (when done)

```bash
deactivate
```

## API Endpoints (Optional - for Frontend Integration)

The API is available if you run the FastAPI server. It's not needed if you're just using `python generate.py`.

- `GET /` - Health check
- `GET /certificates` - Retrieve all certificates from data source
- `POST /generate` - Generate PDF certificates for all entries in organized folder structure
- `DELETE /clear` - Clear all generated certificates and reset the output directory

## Using the API

### Method 1: Using Browser (for GET requests)

1. Health check: Visit `http://localhost:8000/` in your browser
2. View certificates: Visit `http://localhost:8000/certificates` to see your data

### Method 2: Using cURL (Command Line)

**View certificates:**

```bash
curl http://localhost:8000/certificates
```

**Generate certificates:**

```bash
curl -X POST http://localhost:8000/generate
```

**Clear all certificates:**

```bash
curl -X DELETE http://localhost:8000/clear
```

### Method 3: Using REST Client (Recommended for Testing)

Install a REST client like Postman, Insomnia, or use VS Code REST Client extension, then:

1. **GET** `http://localhost:8000/` → Health check
2. **GET** `http://localhost:8000/certificates` → View data
3. **POST** `http://localhost:8000/generate` → Generate certificates
4. **DELETE** `http://localhost:8000/clear` → Clear outputs

## Data format

Input data format (`data/input.json`):

```json
[
  {
    "name": "John Doe",
    "position": "Captain",
    "sport": "Football",
    "date": "March 2026"
  }
]
```

## Certificate generation

- Uses `templates/certificate_base.png` as template
- Applies custom font `templates/GreatVibes-Regular.ttf`
- Handles name truncation for long names (max 20 characters for display)
- Output structure: organized by sport in separate folders
  - Example: `output/Basketball/`, `output/Swimming/`, `output/Weightlifting/`
- File naming format: `name_sport_position.pdf`
  - Example: `Disha_Jain_Basketball_first.pdf`
- Fields positioned on template:
  - Name: (355, 260)
  - Position: (80, 290)
  - Sport: (420, 290)
  - Date: (240, 320)

## Workflow

1. Add certificate data to `data/input.json`
2. Run `python generate.py` to create certificates organized by sport
3. Certificates are saved in `output/[Sport]/name_sport_position.pdf`
4. Run `python generate.py --clear` to remove all generated certificates and start fresh

## Quick Start (Fastest Way)

After completing setup (venv + dependencies):

```bash
# Generate certificates in one command
python generate.py

# Output appears in output/ folder organized by sport
```

That's it! Check the `output/` folder to see your generated PDFs organized by sport.

## Complete Example Workflow

### Using Command Line (Simpler)

1. **Prepare data:**
   - Edit `data/input.json` with certificate information

2. **Generate certificates:**

   ```bash
   python generate.py
   ```

3. **Find generated files:**
   - Navigate to `output/` folder
   - Check subdirectories like `Basketball/`, `Swimming/`, etc.
   - PDFs are named: `name_sport_position.pdf`

4. **Generate new batch:**
   ```bash
   python generate.py --clear-gen
   ```

### Using API (For Frontend Integration)

1. **Prepare data:**
   - Edit `data/input.json` with certificate information

2. **Start server:**

   ```bash
   # Terminal 1
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Check data:**

   ```bash
   # Terminal 2 (new terminal, keep first one running)
   curl http://localhost:8000/certificates
   ```

4. **Generate certificates:**

   ```bash
   curl -X POST http://localhost:8000/generate
   ```

5. **Find generated files:**
   - Navigate to `output/` folder
   - Check subdirectories like `Basketball/`, `Swimming/`, etc.
   - PDFs are named: `name_sport_position.pdf`

6. **Generate new batch (clear old ones first):**
   ```bash
   curl -X DELETE http://localhost:8000/clear
   # Then update data/input.json and regenerate
   curl -X POST http://localhost:8000/generate
   ```

## Troubleshooting

### "Module not found" error

- Ensure virtual environment is activated: You should see `(venv)` in terminal
- Reinstall dependencies: `pip install -r requirements.txt`

### Port 8000 already in use

- Stop the current server with `Ctrl+C`
- Or use a different port: `uvicorn app.main:app --reload --port 8001`

### Certificate not generating

- Check `data/input.json` format (must have "name", "position", "sport", "date" fields)
- Ensure template files exist:
  - `templates/certificate_base.png`
  - `templates/GreatVibes-Regular.ttf`

### No output folder

- The `output/` folder is created automatically when you generate certificates
- If it doesn't exist or is empty, ensure you called the `/generate` endpoint
