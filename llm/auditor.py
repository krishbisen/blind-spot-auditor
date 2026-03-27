"""
llm/auditor.py
--------------
THE MULTI-TOOL BRAIN.
Includes full test execution for all 3 clinical tools.
"""

import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=os.getenv("HF_API_KEY")
)

SYSTEM_PROMPT = """You are a Senior Diagnostic Physician AI expert. Your role is to be a clinical 'Red-Teamer' who identifies diagnostic blind spots by carefully auditing patient charts."""

# ─────────────────────────────────────────────
# TOOLS (Logic remains the same)
# ─────────────────────────────────────────────

def audit_patient_blind_spots(patient_data: dict) -> str:
    chart = build_patient_context(patient_data)
    prompt = f"{chart}\n\n=== TASK ===\nPerform a Diagnostic Blind Spot Audit. Identify what the clinical team might be missing."
    return _call_huggingface_api(prompt)

def check_medication_safety(patient_data: dict) -> str:
    chart = build_patient_context(patient_data)
    prompt = f"{chart}\n\n=== TASK ===\nReview current medications and allergies for safety risks."
    return _call_huggingface_api(prompt)

def analyze_clinical_trends(patient_data: dict) -> str:
    chart = build_patient_context(patient_data)
    prompt = f"{chart}\n\n=== TASK ===\nAnalyze lab trends and visit notes for progression or decline."
    return _call_huggingface_api(prompt)

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def build_patient_context(p: dict) -> str:
    context = f"PATIENT: {p['patient']['name']}, {p['patient']['age']}y {p['patient']['gender']}\n"
    context += f"CURRENT DX: {p['current_diagnosis']['condition']}\n"
    context += "LABS: " + ", ".join([f"{l['test']}: {l['value']}" for l in p.get('lab_results', [])]) + "\n"
    if 'visit_notes' in p:
        context += "VISIT NOTES: " + " | ".join([n['note'] for n in p['visit_notes']]) + "\n"
    return context

def _call_huggingface_api(prompt: str) -> str:
    try:
        response = client.chat_completion(
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ─────────────────────────────────────────────
# 🚀 FULL TEST EXECUTION BLOCK
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Test with Priya Sharma's data
    file_path = os.path.join("data", "synthetic_patient.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        
        print(f"\n=== TESTING ALL TOOLS FOR: {data['patient']['name']} ===\n")

        print("1. [TESTING] audit_patient_blind_spots...")
        print(audit_patient_blind_spots(data))
        print("-" * 50)

        print("2. [TESTING] check_medication_safety...")
        print(check_medication_safety(data))
        print("-" * 50)

        print("3. [TESTING] analyze_clinical_trends...")
        print(analyze_clinical_trends(data))
        print("-" * 50)
        
        print("\n✅ ALL LOCAL TESTS COMPLETED.")
    else:
        print(f"❌ Error: {file_path} not found. Please check your data folder.")