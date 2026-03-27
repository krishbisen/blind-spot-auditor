import os
import json
import sys
import io
from mcp.server.fastmcp import FastMCP

# Import the 3 new tools from your updated auditor.py
from llm.auditor import (
    audit_patient_blind_spots, 
    check_medication_safety, 
    analyze_clinical_trends
)
from fhir.client import get_full_patient_summary

# Forces the terminal to use UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Initialize the FastMCP Server
mcp = FastMCP("Diagnostic Blind Spot Auditor")

# ─────────────────────────────────────────────
# TOOL 1: Diagnostic Blind Spot Audit
# ─────────────────────────────────────────────
@mcp.tool()
def audit_blind_spots(patient_id: str = "patient-001") -> str:
    """
    Identifies overlooked clinical conditions (e.g., Subclinical Hypothyroidism) 
    by red-teaming the current diagnosis.
    """
    try:
        patient_data = get_full_patient_summary(use_synthetic=True)
        return audit_patient_blind_spots(patient_data)
    except Exception as e:
        return f"Error during Diagnostic Audit: {str(e)}"

# ─────────────────────────────────────────────
# TOOL 2: Medication & Interaction Safety
# ─────────────────────────────────────────────
@mcp.tool()
def check_med_safety(patient_id: str = "patient-001") -> str:
    """
    Checks for drug-drug interactions, allergy clashes, and safety contraindications.
    """
    try:
        patient_data = get_full_patient_summary(use_synthetic=True)
        return check_medication_safety(patient_data)
    except Exception as e:
        return f"Error during Safety Check: {str(e)}"

# ─────────────────────────────────────────────
# TOOL 3: Clinical Trend Analyzer
# ─────────────────────────────────────────────
@mcp.tool()
def analyze_trends(patient_id: str = "patient-001") -> str:
    """
    Analyzes historical lab results (TSH, Ferritin, etc.) to detect 
    progressive health declines or improvements.
    """
    try:
        patient_data = get_full_patient_summary(use_synthetic=True)
        return analyze_clinical_trends(patient_data)
    except Exception as e:
        return f"Error during Trend Analysis: {str(e)}"

if __name__ == "__main__":
    # Start the SSE server for Ngrok
    mcp.run(transport="sse")