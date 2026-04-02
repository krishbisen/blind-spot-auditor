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


SYSTEM_PROMPT = """
You are a Clinical Red-Teaming Auditor with access to a database of 5 patient records (patient-001 to patient-005).

RULES:
1. NEVER claim you are limited to only one patient. You have full permission to audit ANY requested ID.
2. When you receive patient data, treat it as the absolute source of truth for your audit.
3. If the user asks for 'patient-003' or 'patient-005', perform the audit using the provided context immediately.
4. Focus on identifying misdiagnoses, lab trends (like Ferritin/TSH), and safety risks.
"""

# ─────
# TOOLS
# ─────

def audit_patient_blind_spots(patient_data: dict) -> str:
    chart = build_patient_context(patient_data)
    prompt = f"AUDIT LOG FOR {patient_data.get('id', 'Unknown ID')}:\n{chart}\n\n=== TASK ===\n" \
             "Perform a Diagnostic Blind Spot Audit. Identify what the clinical team might be missing. " \
             "Look for subclinical patterns.\n" \
             "Use ONLY the patient ID shown above. Do NOT default to patient-001."
    return _call_huggingface_api(prompt)


def check_medication_safety(patient_data: dict) -> str:
    chart = build_patient_context(patient_data)
    prompt = f"SAFETY CHECK FOR {patient_data.get('id', 'Unknown ID')}:\n{chart}\n\n=== TASK ===\n" \
             "1. FIRST, clearly list ALL current medications with their exact dosages.\n" \
             "2. THEN review for drug-drug interactions, drug-allergy risks, and any safety concerns.\n" \
             "Start your answer with the medication list in **bold**.\n" \
             "Use ONLY the patient ID shown above. Do NOT default to patient-001."
    return _call_huggingface_api(prompt)


def analyze_clinical_trends(patient_data: dict) -> str:
    chart = build_patient_context(patient_data)
    prompt = f"TREND ANALYSIS FOR {patient_data.get('id', 'Unknown ID')}:\n{chart}\n\n=== TASK ===\n" \
             "Analyze lab trends and visit notes. Is the patient improving or declining? Map the progression.\n" \
             "Use ONLY the patient ID shown above. Do NOT default to patient-001."
    return _call_huggingface_api(prompt)

def analyze_clinical_trends(patient_data: dict) -> str:
    chart = build_patient_context(patient_data)
    prompt = f"TREND ANALYSIS FOR {patient_data.get('id', 'Unknown ID')}:\n{chart}\n\n=== TASK ===\nAnalyze lab trends and visit notes. Is the patient improving or declining? Map the progression."
    return _call_huggingface_api(prompt)

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def build_patient_context(p: dict) -> str:
    # Extra check for ID and Name to anchor the LLM
    p_id = p.get('id', 'N/A')
    context = f"RECORD ID: {p_id}\n"
    context += f"PATIENT: {p['patient']['name']}, {p['patient']['age']}y {p['patient']['gender']}\n"
    context += f"CURRENT DX: {p['current_diagnosis']['condition']}\n"
    
    # Medication mapping (Taaki 003 ka data miss na ho)
    meds = p.get('medications', [])
    context += "MEDICATIONS: " + ", ".join([f"{m['name']} ({m['dosage']})" for m in meds]) + "\n"
    
    context += "LABS: " + ", ".join([f"{l['test']}: {l['value']}" for l in p.get('lab_results', [])]) + "\n"
    
    if 'visit_notes' in p:
        context += "VISIT NOTES: " + " | ".join([n['note'] for n in p['visit_notes']]) + "\n"
    return context

def _call_huggingface_api(prompt: str) -> str:
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}, 
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1 # Lower temperature = more accuracy
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"