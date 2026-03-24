import os
import json
from mcp.server.fastmcp import FastMCP
from llm.auditor import run_diagnostic_audit
from fhir.client import get_full_patient_summary
import sys
import io

# Forces the terminal to use UTF-8 so emojis and symbols don't crash it
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Initialize the FastMCP Server
mcp = FastMCP("Diagnostic Blind Spot Auditor")

@mcp.tool()
def audit_patient(patient_id: str = "patient-001") -> str:
    """
    Performs a diagnostic red-team audit on a patient's FHIR record 
    to identify potential misdiagnoses and clinical blind spots.
    """
    try:
        # Step A: Fetch the data (uses your Week 1 code)
        # Note: For the hackathon, we use 'use_synthetic=True' for demos
        patient_data = get_full_patient_summary(use_synthetic=True)
        
        # Step B: Run the AI Audit (uses your Week 2 logic)
        report = run_diagnostic_audit(patient_data, llm_provider="huggingface")
        
        return report
    except Exception as e:
        return f"Error during audit: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="sse")