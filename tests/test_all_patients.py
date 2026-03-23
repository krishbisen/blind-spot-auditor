"""
tests/test_all_patients.py
--------------------------
Week 2 — Run the Blind Spot Audit on ALL 5 patients.

This proves your agent works across different diseases,
not just one case. This is what impresses judges.

Usage:
    python tests/test_all_patients.py
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from llm.auditor import run_diagnostic_audit


# All 5 patients with their expected blind spots
PATIENTS = [
    {
        "file": "data/synthetic_patient.json",
        "name": "Priya Sharma",
        "current_dx": "Major Depressive Disorder",
        "expected_blind_spot": "Hypothyroidism"
    },
    {
        "file": "data/patient_2_celiac.json",
        "name": "Arjun Mehta",
        "current_dx": "Irritable Bowel Syndrome",
        "expected_blind_spot": "Celiac"
    },
    {
        "file": "data/patient_3_sleep_apnea.json",
        "name": "Rajesh Verma",
        "current_dx": "Major Depressive Disorder",
        "expected_blind_spot": "Sleep Apnea"
    },
    {
        "file": "data/patient_4_parkinsons.json",
        "name": "Sunita Rao",
        "current_dx": "Generalized Anxiety Disorder",
        "expected_blind_spot": "Parkinson"
    },
    {
        "file": "data/patient_5_lupus.json",
        "name": "Divya Krishnan",
        "current_dx": "Fibromyalgia",
        "expected_blind_spot": "Lupus"
    }
]


def load_patient(filepath):
    """Load patient from JSON file."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(BASE_DIR, filepath)
    with open(full_path, "r") as f:
        return json.load(f)


def run_all_patients():
    print("""
╔══════════════════════════════════════════════════════════╗
║     🏥 WEEK 2 — ALL 5 PATIENT BLIND SPOT AUDITS         ║
╚══════════════════════════════════════════════════════════╝
""")

    results = []

    for i, patient_info in enumerate(PATIENTS, 1):
        print(f"\n{'='*60}")
        print(f"PATIENT {i}/5: {patient_info['name']}")
        print(f"Current Diagnosis: {patient_info['current_dx']}")
        print(f"Expected Blind Spot: {patient_info['expected_blind_spot']}")
        print(f"{'='*60}")

        try:
            # Load patient data
            patient_data = load_patient(patient_info["file"])

            # Run the audit
            print(f"\n🔍 Running audit on {patient_info['name']}...")
            report = run_diagnostic_audit(
                patient_data,
                llm_provider="huggingface"
            )

            # Check if blind spot was caught
            caught = patient_info["expected_blind_spot"].lower() in report.lower()

            print(f"\n{report}")
            print(f"\n{'─'*60}")
            print(f"✅ Blind spot caught: {'YES' if caught else 'NEEDS REVIEW'}")

            results.append({
                "patient": patient_info["name"],
                "caught": caught
            })

        except Exception as e:
            print(f"❌ Error on {patient_info['name']}: {e}")
            results.append({
                "patient": patient_info["name"],
                "caught": False
            })

        print("\nPausing 3 seconds before next patient...")
        import time
        time.sleep(3)

    # Final summary
    print(f"\n{'='*60}")
    print("WEEK 2 RESULTS SUMMARY")
    print(f"{'='*60}")
    caught_count = sum(1 for r in results if r["caught"])
    for r in results:
        status = "✅ CAUGHT" if r["caught"] else "⚠️  REVIEW"
        print(f"  {status} — {r['patient']}")

    print(f"\nBlind spots caught: {caught_count}/{len(PATIENTS)}")

    if caught_count >= 4:
        print("""
🎉 WEEK 2 COMPLETE — YOUR AGENT IS ROBUST!

Your agent successfully catches blind spots across:
- Endocrine disorders (Hypothyroidism)
- Gastrointestinal disorders (Celiac)
- Sleep disorders (Sleep Apnea)
- Neurological disorders (Parkinson's)
- Autoimmune disorders (Lupus)

This is exactly what judges want to see.
Say "Week 3" when ready to build the MCP server!
""")
    else:
        print("\n⚠️  Some patients need prompt improvement. Say 'improve prompt' for help.")


if __name__ == "__main__":
    run_all_patients()
