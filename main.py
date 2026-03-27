"""
main.py
-------
Diamond Diagnostic Auditor - Main Entry Point.
This script demonstrates the core auditing logic using FHIR data and LLM analysis.
"""

import sys
import os

# Ensure local modules are accessible
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fhir.client import get_full_patient_summary
from llm.auditor import audit_patient_blind_spots as run_diagnostic_audit

def print_banner():
    """Prints a clean, professional banner for the terminal."""
    print("=" * 60)
    print("         DIAMOND DIAGNOSTIC BLIND SPOT AUDITOR")
    print("        Automated Clinical Red-Teaming System")
    print("=" * 60)

def run_audit(patient_id="patient-001"):
    """Orchestrates the data loading and auditing process."""
    print(f"\n[SYSTEM] Initializing audit for: {patient_id}...")
    
    # 1. Fetch Patient Context
    patient_data = get_full_patient_summary(patient_id=patient_id, use_synthetic=True)
    
    if not patient_data:
        print(f" Error: Patient record '{patient_id}' not found.")
        return

    name = patient_data.get('patient', {}).get('name', 'Unknown')
    dx = patient_data.get('current_diagnosis', {}).get('condition', 'N/A')
    
    print(f"  > Target: {name}")
    print(f"  > Current DX: {dx}")

    # 2. Execute LLM Analysis
    print("\n" + "-" * 40)
    print("[AI ENGINE] Analyzing for diagnostic blind spots...")
    report = run_diagnostic_audit(patient_data)
    
    # 3. Output Findings
    print("\n" + "═" * 60)
    print("                FINAL AUDIT REPORT")
    print("═" * 60)
    print(report)
    print("═" * 60)
    print("\n[COMPLETE] Audit finished successfully.")

def main():
    print_banner()
    
    # Run audit for the primary case
    # To test other patients, change to patient-002, 003, etc.
    run_audit("patient-001")

if __name__ == "__main__":
    main()