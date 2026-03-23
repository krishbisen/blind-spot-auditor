"""
main.py
-------
RUN THIS FIRST.

This is the entry point for your Diagnostic Blind Spot Auditor.
It connects the FHIR client → LLM auditor → prints the report.

Usage:
    python main.py
"""

import sys
import os

# Make sure Python finds our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fhir.client import get_full_patient_summary
from llm.auditor import run_diagnostic_audit


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║        💎 DIAGNOSTIC BLIND SPOT AUDITOR                 ║
║        Agents Assemble Hackathon 2026                   ║
║        "What is everyone assuming is correct            ║
║         that might actually be wrong?"                  ║
╚══════════════════════════════════════════════════════════╝
""")


def main():
    print_banner()
    
    # ─── STEP 1: Load Patient Data ───
    print("STEP 1: Loading patient data from FHIR...\n")
    patient_data = get_full_patient_summary(use_synthetic=True)
    
    patient_name = patient_data['patient']['name']
    current_dx = patient_data['current_diagnosis']['condition']
    months = patient_data['current_diagnosis']['duration_months']
    
    print(f"\n  Patient:           {patient_name}")
    print(f"  Current Diagnosis: {current_dx}")
    print(f"  Time on Treatment: {months} months")
    print(f"  Treatment Response: {patient_data['treatment_response']['response_level']}")
    
    # ─── STEP 2: Run the Blind Spot Audit ───
    print("\n" + "─" * 60)
    print("STEP 2: Running Diagnostic Blind Spot Audit...\n")
    print("  The LLM will now red-team the current diagnosis.")
    print("  It will look for what everyone might be missing.\n")
    
    # Change llm_provider to "openai" if you have an OpenAI key
    # Change to "anthropic" if you have an Anthropic key
    # It will use a mock response if no key is found (still shows you the output)
    report = run_diagnostic_audit(patient_data, llm_provider="huggingface")
    
    # ─── STEP 3: Display the Report ───
    print("\n" + "═" * 60)
    print("  BLIND SPOT AUDIT REPORT")
    print("═" * 60)
    print(report)
    print("═" * 60)
    
    print(f"""
✅ WEEK 1 COMPLETE — YOUR AGENT IS WORKING.

What just happened:
  1. You read patient data from FHIR format ✓
  2. You fed it to an LLM with a diagnostic red-team prompt ✓
  3. The LLM produced a structured Blind Spot Report ✓

This is the core of your hackathon submission.
Week 2: Improve the prompt + test 5 different patients.
Week 3: Wrap this in an MCP server.

Come back to Claude and say "Week 2" when you are ready.
""")


if __name__ == "__main__":
    main()
