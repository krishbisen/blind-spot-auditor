import os
import json
import sys
import io
from mcp.server.fastmcp import FastMCP

from llm.auditor import (
    audit_patient_blind_spots, 
    check_medication_safety, 
    analyze_clinical_trends
)
from fhir.client import get_full_patient_summary

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

mcp = FastMCP("Diagnostic Blind Spot Auditor")

# ─────────────────────────────────────────────
# TOOL 1: Diagnostic Blind Spot Audit
# ─────────────────────────────────────────────
@mcp.tool()
async def audit_blind_spots(patient_id: str = "patient-001") -> str:
    """
    Identifies overlooked clinical conditions by red-teaming the current diagnosis.
    """
    try:
        patient_data = get_full_patient_summary(patient_id=patient_id, use_synthetic=True)
        return audit_patient_blind_spots(patient_data)
    except Exception as e:
        return f"Error during Diagnostic Audit: {str(e)}"

# ─────────────────────────────────────────────
# TOOL 2: Medication & Interaction Safety  ← NOW SUPER CLEAR FOR YOUR QUERY
# ─────────────────────────────────────────────
@mcp.tool()
async def check_med_safety(patient_id: str = "patient-001") -> str:
    """
    Tool to retrieve and list the current medications of ANY patient (patient-001 to patient-005).
    
    Use this tool when the user asks for:
    - "give me the medication of patient-XXX"
    - "what medicines is patient-004 taking"
    - "medication list for patient-004"
    - "meds of patient-004 right now"
    - any question about medications, drugs, or prescriptions.
    
    It always returns the full list of medications with dosages first, then does a safety review (interactions, allergies, risks).
    """
    try:
        patient_data = get_full_patient_summary(patient_id=patient_id, use_synthetic=True)
        return check_medication_safety(patient_data)
    except Exception as e:
        return f"Error during Safety Check: {str(e)}"

# ─────────────────────────────────────────────
# TOOL 3: Clinical Trend Analyzer
# ─────────────────────────────────────────────
@mcp.tool()
async def analyze_trends(patient_id: str = "patient-001") -> str:
    """
    Analyzes historical lab results to detect health declines or improvements.
    """
    try:
        patient_data = get_full_patient_summary(patient_id=patient_id, use_synthetic=True)
        return analyze_clinical_trends(patient_data)
    except Exception as e:
        return f"Error during Trend Analysis: {str(e)}"

if __name__ == "__main__":
    print("🚀 Starting MCP Server with 3 clinical tools...")
    print("   • audit_blind_spots")
    print("   • check_med_safety     ← now optimized for medication queries")
    print("   • analyze_trends")
    mcp.run(transport="sse")