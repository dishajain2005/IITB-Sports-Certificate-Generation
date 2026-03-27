from fastapi import FastAPI
import json
from app.generator import generate_certificate, clear_output_directory

app = FastAPI()

DATA_PATH = "data/input.json"


@app.get("/")
def home():
    return {"message": "Certificate Generator API Running"}


@app.get("/certificates")
def get_certificates():
    with open(DATA_PATH) as f:
        data = json.load(f)
    return data


@app.post("/generate")
def generate_all():
    with open(DATA_PATH) as f:
        data = json.load(f)

    results = []

    for entry in data:
        path = generate_certificate(entry)
        results.append({
            "name": entry["name"],
            "sport": entry["sport"],
            "position": entry["position"],
            "file": path
        })

    return {"generated": results}


@app.delete("/clear")
def clear_outputs():
    return clear_output_directory()