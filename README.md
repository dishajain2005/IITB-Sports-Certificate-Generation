# IITB Sports Certificate Generation

## Overview

FastAPI backend for JSON-driven certificate generation matching the Figma design semantics.

## Setup

1. Create and activate Python venv.
2. `pip install -r requirements.txt`

## Run server

`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## API

- GET `/` : health check
- GET `/api/v1/certificates` : all certificates (API-ready design map)
- GET `/api/v1/certificates/{cert_id}` : specific item
- GET `/api/v1/certificates/{cert_id}/ui-mapping` : per-component UI mapping for front-end
- POST `/api/v1/certificates/{cert_id}/generate` : generate JSON + PNG artifact
- GET `/api/v1/certificates/{cert_id}/artifact` : download generated PNG

## Data flow

1. JSON source: `data/sample_certificates.json`
2. Load as `CertificateRaw` objects in `app/data_loader.py`
3. Transform to API-ready model `CertificateAPIVersion` in `app/data_loader.py`:
   - includes headline, body, metadata, per-component style hints
4. Endpoint serve from `app/main.py`
5. Artifact generation in `/generate` uses Pillow image builder

## Frontend plug-in

Frontend can call:

- `/api/v1/certificates` for list screen
- `/api/v1/certificates/{id}/ui-mapping` to render title/body/sign fields like Figma
- use generated image URL `/api/v1/certificates/{id}/artifact` as preview
