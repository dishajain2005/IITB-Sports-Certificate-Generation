from fastapi import FastAPI, HTTPException
import json
from app.generator import generate_certificate, clear_output_directory
from app.schema import CertificateData

app = FastAPI(title="IIT Bombay Certificate Generator")

DATA_PATH = "data/input.json"


@app.get("/")
def home():
    return {"message": "Certificate Generator API Running"}


@app.get("/certificates")
def get_certificates():
    with open(DATA_PATH) as f:
        data = json.load(f)
    return data


@app.post("/generate/single")
def generate_single(data: CertificateData):
    """Generate one certificate from a JSON body."""
    path = generate_certificate(data.model_dump())
    return {"file": path, **data.model_dump()}


@app.post("/generate")
def generate_all():
    """Generate certificates for every entry in data/input.json."""
    with open(DATA_PATH) as f:
        entries = json.load(f)

    results = []
    for entry in entries:
        path = generate_certificate(entry)
        results.append({"file": path, **entry})

    return {"generated": results, "count": len(results)}


@app.delete("/clear")
def clear_outputs():
    return clear_output_directory()