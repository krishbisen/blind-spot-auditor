"""
fhir/client.py
--------------
Connects to synthetic clinical datasets (patient-001 to patient-005).
"""
import requests
import json
import os

FHIR_BASE_URL = "https://hapi.fhir.org/baseR4"

def get_full_patient_summary(patient_id: str = "patient-001", use_synthetic: bool = True) -> dict:
    if not use_synthetic:
        # Live FHIR (still dummy for demo)
        return {"patient": {"name": "Live FHIR Patient"}, "current_diagnosis": {"condition": "Unknown"}, "lab_results": []}

    file_map = {
        "patient-001": "synthetic_patient.json",
        "patient-002": "patient_2_celiac.json",
        "patient-003": "patient_3_sleep_apnea.json",
        "patient-004": "patient_4_parkinsons.json",
        "patient-005": "patient_5_lupus.json"
    }

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = file_map.get(patient_id, "synthetic_patient.json")
    file_path = os.path.join(BASE_DIR, "data", file_name)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✓ Loaded synthetic data for {patient_id} from {file_name}")  # ← debug
        return data
    except FileNotFoundError:
        print(f" File {file_name} not found for {patient_id} → falling back to synthetic_patient.json")
        fallback_path = os.path.join(BASE_DIR, "data", "synthetic_patient.json")
        with open(fallback_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f" Error loading patient data: {e}")
        raise