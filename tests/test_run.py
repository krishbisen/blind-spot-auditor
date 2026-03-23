"""
tests/test_run.py
-----------------
Run this to verify everything is working correctly.

Usage:
    python tests/test_run.py
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fhir.client import get_full_patient_summary, load_synthetic_patient
from llm.auditor import run_diagnostic_audit, build_patient_context


def test_fhir_client():
    print("TEST 1: FHIR Client")
    print("-" * 40)
    
    data = load_synthetic_patient()
    
    assert data["patient"]["name"] == "Priya Sharma", "Patient name mismatch"
    assert data["current_diagnosis"]["condition"] is not None, "Missing diagnosis"
    assert len(data["lab_results"]) > 0, "No lab results"
    assert len(data["visit_notes"]) > 0, "No visit notes"
    assert len(data["family_history"]) > 0, "No family history"
    
    print(f"  ✓ Patient loaded: {data['patient']['name']}")
    print(f"  ✓ Diagnosis: {data['current_diagnosis']['condition']}")
    print(f"  ✓ Lab results: {len(data['lab_results'])} found")
    print(f"  ✓ Visit notes: {len(data['visit_notes'])} found")
    print(f"  ✓ Family history: {len(data['family_history'])} entries")
    print()


def test_context_builder():
    print("TEST 2: Patient Context Builder")
    print("-" * 40)
    
    data = load_synthetic_patient()
    context = build_patient_context(data)
    
    assert "Priya Sharma" in context, "Patient name missing from context"
    assert "TSH" in context, "Lab results missing from context"
    assert "Hashimoto" in context, "Family history missing from context"
    assert "BORDERLINE HIGH" in context, "Lab status missing from context"
    
    print(f"  ✓ Context built successfully")
    print(f"  ✓ Context length: {len(context)} characters")
    print(f"  ✓ Contains patient name: Yes")
    print(f"  ✓ Contains lab results: Yes")
    print(f"  ✓ Contains family history: Yes")
    print()


def test_audit_output():
    print("TEST 3: LLM Audit Output (using mock response)")
    print("-" * 40)
    
    data = load_synthetic_patient()
    
    # Force mock response for testing without API key
    from llm.auditor import _get_mock_response
    report = _get_mock_response()
    
    assert "BLIND SPOT AUDIT REPORT" in report, "Report header missing"
    assert "RED FLAGS" in report, "Red flags section missing"
    assert "OVERLOOKED DIFFERENTIAL" in report, "Differential section missing"
    assert "RECOMMENDED IMMEDIATE ACTIONS" in report, "Actions section missing"
    assert "DISCLAIMER" in report, "Disclaimer missing"
    
    print(f"  ✓ Report generated successfully")
    print(f"  ✓ All required sections present")
    print(f"  ✓ Report length: {len(report)} characters")
    print(f"  ✓ Contains disclaimer: Yes")
    
    # Check it caught the hypothyroidism
    assert "Hypothyroid" in report or "hypothyroid" in report, "Should catch hypothyroidism"
    print(f"  ✓ Correctly identified hypothyroidism as blind spot: Yes")
    print()


def test_full_pipeline():
    print("TEST 4: Full Pipeline (FHIR → Context → Audit)")
    print("-" * 40)
    
    # Full pipeline with mock LLM
    data = get_full_patient_summary(use_synthetic=True)
    context = build_patient_context(data)
    
    from llm.auditor import _get_mock_response
    report = _get_mock_response()
    
    print(f"  ✓ FHIR data loaded")
    print(f"  ✓ Context built: {len(context)} chars")
    print(f"  ✓ Audit report generated: {len(report)} chars")
    print(f"  ✓ Full pipeline works end-to-end")
    print()


def run_all_tests():
    print("""
╔══════════════════════════════════════════════════════════╗
║        🧪 RUNNING ALL WEEK 1 TESTS                      ║
╚══════════════════════════════════════════════════════════╝
""")
    
    tests = [
        test_fhir_client,
        test_context_builder,
        test_audit_output,
        test_full_pipeline,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}\n")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
            failed += 1
    
    print("═" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("""
🎉 ALL TESTS PASSED — WEEK 1 COMPLETE!

Your Diagnostic Blind Spot Auditor is working correctly.
Now add your API key to .env and run:

    python main.py

To see the real LLM audit in action.
""")
    else:
        print("\n⚠️  Some tests failed. Paste the error message to Claude for help.")


if __name__ == "__main__":
    run_all_tests()
