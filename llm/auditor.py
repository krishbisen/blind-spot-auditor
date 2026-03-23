"""
llm/auditor.py
--------------
THE BRAIN OF THE PROJECT.

This file takes a patient's full FHIR data and asks an LLM:
"Given everything we know — what diagnosis might everyone be missing?"

This is the core value of your entire hackathon submission.
The LLM does what no rule-based system can:
it reasons across the full patient narrative and finds the blind spot.
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()


# ─────────────────────────────────────────────
# THE DIAGNOSTIC AUDIT PROMPT
# This is the most important part of your project.
# It instructs the LLM to "red team" the current diagnosis.
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """You are a Senior Diagnostic Physician AI assistant with expertise in identifying diagnostic blind spots — cases where a patient has been given a diagnosis that may be incomplete or incorrect, despite the clinical team's best efforts.

Your role is NOT to replace the clinician. Your role is to be the "brilliant colleague who read the chart more carefully than anyone had time to." You ask questions. You surface overlooked evidence. You say "have you considered...?" — never "you are wrong."

When reviewing a patient case, you:
1. Carefully examine ALL available data — not just the obvious symptoms
2. Look for patterns that do NOT fit the current diagnosis
3. Identify tests that were NOT ordered but should have been
4. Check family history for genetic/autoimmune clues
5. Notice symptoms that were dismissed or attributed to other causes
6. Consider how long the patient has been on treatment and whether response is adequate

Output your analysis as a structured Blind Spot Report. Be specific. Be evidence-based. Cite the exact data points from the patient record that support your concern. Never speculate without evidence."""


def build_patient_context(patient_data: dict) -> str:
    """
    Convert our patient JSON into a clean text summary for the LLM.
    The LLM reads this as the "patient chart."
    """
    
    p = patient_data
    
    context = f"""
=== PATIENT CHART ===
Patient: {p['patient']['name']}, {p['patient']['age']} year old {p['patient']['gender']}

CURRENT DIAGNOSIS: {p['current_diagnosis']['condition']} (ICD: {p['current_diagnosis']['icd_code']})
Diagnosed: {p['current_diagnosis']['diagnosed_date']} ({p['current_diagnosis']['duration_months']} months ago)
Current Medications: {', '.join(p['current_diagnosis']['current_medications'])}

SYMPTOMS AT INITIAL DIAGNOSIS:
{chr(10).join(f"- {s}" for s in p['symptoms_at_diagnosis'])}

LABORATORY RESULTS:
"""
    for lab in p['lab_results']:
        status = lab.get('status', '')
        note = lab.get('note', '')
        value = lab.get('value', 'N/A')
        unit = lab.get('unit', '')
        context += f"- {lab['test']}: {value} {unit}"
        if status:
            context += f" [{status}]"
        if note:
            context += f" — Note: {note}"
        context += "\n"
    
    context += f"""
CLINICAL VISIT NOTES (chronological):
"""
    for visit in p['visit_notes']:
        context += f"- [{visit['date']}] {visit['note']}\n"
    
    context += f"""
FAMILY HISTORY:
{chr(10).join(f"- {h}" for h in p['family_history'])}

TREATMENT RESPONSE:
- Months on current treatment: {p['treatment_response']['months_on_antidepressants']}
- Response: {p['treatment_response']['response_level']}
- Clinician note: {p['treatment_response']['psychiatrist_note']}

ALLERGIES: {', '.join(p['allergies'])}
"""
    
    return context


def run_diagnostic_audit(patient_data: dict, llm_provider: str = "anthropic") -> str:
    """
    THE MAIN FUNCTION.
    
    Sends the patient chart to the LLM and gets back a Blind Spot Report.
    
    Supports both Anthropic (Claude) and OpenAI (GPT-4).
    We use Claude by default since we're building on Anthropic's platform.
    """
    
    patient_context = build_patient_context(patient_data)
    
    audit_request = f"""
{patient_context}

=== YOUR TASK ===
Please perform a Diagnostic Blind Spot Audit on this patient.

Structure your response EXACTLY as follows:

**BLIND SPOT AUDIT REPORT**
Patient: [name and age]
Audit Date: [today]

**CURRENT DIAGNOSIS ASSESSMENT**
[Does the evidence fully support the current diagnosis? What fits? What doesn't?]

**RED FLAGS IN THE RECORD**
[List specific data points from this chart that are inconsistent with or unexplained by the current diagnosis]

**OVERLOOKED DIFFERENTIAL DIAGNOSIS**
[What other condition(s) should be considered? Be specific about which condition and why]

**SUPPORTING EVIDENCE FROM THIS CHART**
[List the exact evidence from the patient's record that supports your alternative diagnosis]

**RECOMMENDED IMMEDIATE ACTIONS**
[What specific tests or consultations should be ordered NOW?]

**CONFIDENCE LEVEL**
[How strong is the evidence for the blind spot? Low / Medium / High — and why]

**IMPORTANT DISCLAIMER**
[Always end with: This audit is a clinical decision support tool. All findings must be reviewed and validated by a licensed physician before any action is taken.]
"""
    
    print("\n🔍 Sending patient chart to LLM for diagnostic audit...")
    print("   This is the moment your agent earns its prize...\n")
    
    if llm_provider == "anthropic":
        return _call_anthropic(audit_request)
    elif llm_provider == "openai":
        return _call_openai(audit_request)
    elif llm_provider == "gemini":
        return _call_gemini(audit_request)
    elif llm_provider == "groq":
        return _call_groq(audit_request) 
    elif llm_provider == "huggingface":
        return _call_huggingface(audit_request)   
    else:
        raise ValueError(f"Unknown LLM provider: {llm_provider}")


def _call_anthropic(prompt: str) -> str:
    """Call Claude (Anthropic) API."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    except ImportError:
        print("Anthropic library not installed. Run: pip install anthropic")
        return _get_mock_response()
    except Exception as e:
        print(f"Anthropic API error: {e}")
        print("Using mock response for testing...")
        return _get_mock_response()


def _call_openai(prompt: str) -> str:
    """Call GPT-4 (OpenAI) API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    except ImportError:
        print("OpenAI library not installed. Run: pip install openai")
        return _get_mock_response()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return _get_mock_response()


def _get_mock_response() -> str:
    """
    A hardcoded mock response for Week 1 testing.
    Use this when you don't have API keys yet.
    Shows you exactly what the real output will look like.
    """
    return """
**BLIND SPOT AUDIT REPORT**
Patient: Priya Sharma, 34 year old female
Audit Date: 2026-03-23

**CURRENT DIAGNOSIS ASSESSMENT**
The current diagnosis of Major Depressive Disorder partially explains the patient's presentation, but several critical findings are inconsistent with a primary psychiatric diagnosis and suggest an underlying organic cause.

**RED FLAGS IN THE RECORD**
- TSH at 4.8 mIU/L is BORDERLINE HIGH and was never followed up with Free T4
- Unexplained cholesterol elevation (224 mg/dL) with no cardiac risk factors
- Progressive weight gain of 8kg with no dietary cause documented
- Cold intolerance mentioned in November 2023 visit — a classic hypothyroid symptom
- Hair thinning noted in September 2023 visit, dismissed as stress
- Hoarse voice reported in May 2024 visit — another hypothyroid red flag
- Mild normocytic anemia unexplained
- 18 months of antidepressant therapy with only 40% improvement — treatment resistance pattern
- Constipation and dry skin noted in February 2024 — both hypothyroid symptoms
- Strong autoimmune family history: mother (Hashimoto's), maternal aunt (hypothyroidism), sister (Type 1 diabetes)

**OVERLOOKED DIFFERENTIAL DIAGNOSIS**
PRIMARY CONCERN: Hypothyroidism / Hashimoto's Thyroiditis

This patient's entire clinical presentation — fatigue, weight gain, cold intolerance, hair thinning, constipation, dry skin, cognitive slowing, low mood, hoarseness, mild anemia, borderline TSH, and elevated cholesterol — maps almost perfectly onto the clinical picture of hypothyroidism, specifically Hashimoto's thyroiditis given the strong family autoimmune history.

**SUPPORTING EVIDENCE FROM THIS CHART**
1. Borderline TSH (4.8 mIU/L) with no Free T4 ordered — this is the single most critical missed step
2. Autoimmune family pattern (Hashimoto's in mother AND aunt, T1DM in sister)
3. Symptom onset timeline consistent with gradual thyroid failure
4. ALL documented symptoms (fatigue, weight gain, cold intolerance, hair loss, hoarseness, constipation, dry skin, cognitive fog, low mood) appear on standard hypothyroidism symptom checklists
5. Treatment-resistant depression is a documented presentation of undiagnosed hypothyroidism
6. Unexplained cholesterol elevation — hypothyroidism is a known secondary cause

**RECOMMENDED IMMEDIATE ACTIONS**
1. URGENT: Order Free T4 and Anti-TPO antibodies (Hashimoto's marker)
2. Repeat TSH with reflex Free T4
3. Thyroid ultrasound if antibodies positive
4. Endocrinology referral
5. Do NOT increase antidepressant dosage until thyroid workup is complete

**CONFIDENCE LEVEL**
HIGH — Multiple independent findings from this patient's own record converge on this diagnosis. The combination of: borderline TSH, 9 classic hypothyroid symptoms documented over 18 months, strong autoimmune family history, treatment-resistant depression, and unexplained metabolic changes (cholesterol, anemia) represents compelling clinical evidence.

**IMPORTANT DISCLAIMER**
This audit is a clinical decision support tool. All findings must be reviewed and validated by a licensed physician before any action is taken. This report does not constitute a diagnosis.
"""


if __name__ == "__main__":
    print("=== Testing LLM Auditor ===\n")
    
    # Load synthetic patient
    with open("data/synthetic_patient.json") as f:
        patient = json.load(f)
    
    # Run the audit
    report = run_diagnostic_audit(patient, llm_provider="anthropic")
    
    print("=" * 60)
    print(report)
    print("=" * 60)
def _call_gemini(prompt: str) -> str:
    """Call Google Gemini API — completely free."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(prompt)
        return response.text
    except ImportError:
        print("Gemini library not installed.")
        return _get_mock_response()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return _get_mock_response()

def _call_groq(prompt: str) -> str:
    """Call Groq API — completely free, works in India."""
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Groq API error: {e}")
        return _get_mock_response()


def _call_huggingface(prompt: str) -> str:
    """Call Hugging Face API — completely free, works in India."""
    try:
        from huggingface_hub import InferenceClient
        
        client = InferenceClient(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            token=os.getenv("HF_API_KEY")
        )
        
        full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
        
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )

        return response.choices[0].message.content

    
    except Exception as e:
        print(f"HuggingFace API error: {e}")
        return _get_mock_response()        


def _call_gemini(prompt: str) -> str:
    """Call Google Gemini API."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            system_instruction=SYSTEM_PROMPT
        )
        response = model.generate_content(prompt)
        return response.text
    
    except ImportError:
        print("Gemini library not installed.")
        return _get_mock_response()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return _get_mock_response()