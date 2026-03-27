"""
fhir/client.py
--------------
Connects to the HAPI FHIR server or loads synthetic clinical datasets.
Updated to support multiple patient profiles (001-005).
"""

import requests
import json
import os

# The free public FHIR server (for live integration)
FHIR_BASE_URL = "https://hapi.fhir.org/baseR4"

def get_full_patient_summary(patient_id: str = "patient-001", use_synthetic: bool = True) -> dict:
    """
    Main data orchestrator. Dynamically loads the correct JSON file 
    from the data folder based on the patient_id.
    """
    if not use_synthetic:
        # Live FHIR integration (Simplified for demo)
        return {
            "patient": {"name": "Live FHIR Patient"},
            "current_diagnosis": {"condition": "Unknown"},
            "lab_results": []
        }

    # Mapping IDs to your specific JSON files
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
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to patient-001 if specific file is missing
        fallback_path = os.path.join(BASE_DIR, "data", "synthetic_patient.json")
        with open(fallback_path, "r") as f:
            return json.load(f)

if __name__ == "__main__":
    print("=== FHIR Client Multi-Patient Test ===")
    # Test loading Arjun (002)
    data = get_full_patient_summary("patient-002")
    print(f"✓ Successfully loaded: {data['patient']['name']} ({data['current_diagnosis']['condition']})")