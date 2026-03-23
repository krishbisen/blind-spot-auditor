"""
fhir/client.py
--------------
This file connects to the FREE public FHIR server and reads patient data.
No signup needed. No real patient data. Safe for testing.

FHIR Server we use: https://hapi.fhir.org/baseR4
Think of it like a hospital database you can query with simple HTTP requests.
"""

import requests
import json


# The free public FHIR server — no API key needed
FHIR_BASE_URL = "https://hapi.fhir.org/baseR4"


def get_patient(patient_id: str) -> dict:
    """
    Fetch a patient's basic info from FHIR.
    Returns their name, age, gender etc.
    """
    url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  Could not connect to FHIR server: {e}")
        print("  Using local synthetic data instead...")
        return None


def get_conditions(patient_id: str) -> list:
    """
    Fetch all diagnoses/conditions for a patient.
    In FHIR, each diagnosis is a 'Condition' resource.
    """
    url = f"{FHIR_BASE_URL}/Condition?patient={patient_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        bundle = response.json()
        
        conditions = []
        if "entry" in bundle:
            for entry in bundle["entry"]:
                resource = entry.get("resource", {})
                condition_text = resource.get("code", {}).get("text", "Unknown condition")
                conditions.append(condition_text)
        
        return conditions
    except Exception as e:
        print(f"  Could not fetch conditions: {e}")
        return []


def get_observations(patient_id: str) -> list:
    """
    Fetch lab results and vital signs for a patient.
    In FHIR, lab results are 'Observation' resources.
    """
    url = f"{FHIR_BASE_URL}/Observation?patient={patient_id}&_count=20"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        bundle = response.json()
        
        observations = []
        if "entry" in bundle:
            for entry in bundle["entry"]:
                resource = entry.get("resource", {})
                obs = {
                    "test": resource.get("code", {}).get("text", "Unknown test"),
                    "value": resource.get("valueQuantity", {}).get("value", "N/A"),
                    "unit": resource.get("valueQuantity", {}).get("unit", ""),
                    "status": resource.get("status", "unknown")
                }
                observations.append(obs)
        
        return observations
    except Exception as e:
        print(f"  Could not fetch observations: {e}")
        return []


def load_synthetic_patient() -> dict:
    """
    Load our local test patient when the FHIR server is unavailable.
    This is the 'Priya Sharma' case — hypothyroidism missed as depression.
    Perfect for our demo.
    """
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(BASE_DIR, "data", "synthetic_patient.json"), "r") as f:
        return json.load(f)


def get_full_patient_summary(patient_id: str = None, use_synthetic: bool = True) -> dict:
    """
    Main function — gets everything we need about a patient.
    
    In Week 1: uses synthetic data (safe, no real patients)
    In Week 3+: switches to live FHIR server with real structure
    """
    
    if use_synthetic:
        print("Loading synthetic patient data (Priya Sharma)...")
        patient_data = load_synthetic_patient()
        print(f"Patient loaded: {patient_data['patient']['name']}, age {patient_data['patient']['age']}")
        return patient_data
    
    # Live FHIR path (Week 3+)
    print(f"Fetching patient {patient_id} from FHIR server...")
    
    patient = get_patient(patient_id)
    conditions = get_conditions(patient_id)
    observations = get_observations(patient_id)
    
    return {
        "patient": patient,
        "conditions": conditions,
        "observations": observations
    }


# Quick test — run this file directly to check FHIR connection
if __name__ == "__main__":
    print("=== Testing FHIR Client ===\n")
    
    # Test 1: Load synthetic patient
    data = get_full_patient_summary(use_synthetic=True)
    print(f"\nCurrent diagnosis: {data['current_diagnosis']['condition']}")
    print(f"Duration: {data['current_diagnosis']['duration_months']} months")
    print(f"Labs with issues: {[l['test'] for l in data['lab_results'] if l.get('status') in ['BORDERLINE HIGH', 'ABNORMAL', 'LOW', 'ELEVATED']]}")
    
    # Test 2: Try live FHIR server
    print("\n\nTesting live FHIR server connection...")
    live_patient = get_patient("592776")  # A known test patient on HAPI
    if live_patient:
        print(f"Live FHIR connection works!")
    else:
        print("Live FHIR not available right now — synthetic data is fine for Week 1.")
