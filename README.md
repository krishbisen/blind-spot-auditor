# 💎 Diagnostic Blind Spot Auditor
### Agents Assemble Hackathon 2026 — Your Submission

An MCP tool that reads a patient's full FHIR history and asks:
> "Given everything we know about this patient — what diagnosis might everyone be assuming is correct, but is actually wrong?"

---

## 📁 Project Structure

```
blind-spot-auditor/
├── fhir/
│   └── client.py          ← Reads patient data from FHIR server
├── llm/
│   └── auditor.py         ← The LLM brain — red-teams the diagnosis
├── mcp/
│   └── server.py          ← Wraps everything as an MCP tool (Week 3)
├── data/
│   └── synthetic_patient.json  ← Fake patient for testing
├── tests/
│   └── test_run.py        ← Run this to see it all work end-to-end
├── main.py                ← Entry point — run this first
└── requirements.txt       ← Python packages to install
```

---

## ⚡ Week 1 Goals (Mar 23–30)

- [ ] Install requirements
- [ ] Run `main.py` and see a patient record printed
- [ ] Run `tests/test_run.py` and see the LLM audit output
- [ ] Understand what FHIR is and how data flows
- [ ] Explore Prompt Opinion platform

---

## 🚀 Setup — Do This First

### Step 1 — Install Python packages
```bash
pip install requests openai python-dotenv
```

### Step 2 — Create a .env file in this folder
```
OPENAI_API_KEY=your_key_here
```
> Get a free API key at platform.openai.com
> Or use Anthropic: ANTHROPIC_API_KEY=your_key_here

### Step 3 — Run main.py
```bash
python main.py
```

### Step 4 — Run the full audit test
```bash
python tests/test_run.py
```

---

## 🏥 What is FHIR?

FHIR (Fast Healthcare Interoperability Resources) is the standard format
hospitals use to store and share patient data. Think of it as JSON files
that describe a patient — their conditions, medications, lab results,
allergies, visit history.

We use a FREE public FHIR server for testing:
https://hapi.fhir.org/baseR4

No signup needed. No real patient data. Perfect for our demo.

---

## 🧠 How the Blind Spot Auditor Works

1. We fetch a patient's data from FHIR (conditions, meds, labs, notes)
2. We send ALL of it to an LLM with a special "red team" prompt
3. The LLM looks for inconsistencies between the diagnosis and the evidence
4. It surfaces: "Here's what everyone might be missing..."
5. Output is a clean Blind Spot Report the doctor can act on

---

## 📅 Full Timeline

| Week | Goal |
|------|------|
| 1 | FHIR setup + first patient read + LLM audit working |
| 2 | Improve prompts + test 5 patient profiles |
| 3 | Wrap as MCP server + connect to Prompt Opinion |
| 4 | Test edge cases + publish to marketplace |
| 5–7 | Demo video + submission writeup + submit |
