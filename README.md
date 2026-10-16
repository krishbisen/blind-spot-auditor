# Diagnostic Blind Spot Auditor

![Python](https://img.shields.io/badge/Language-Python-blue.svg)
[![Model Context Protocol](https://img.shields.io/badge/Protocol-MCP-purple.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An AI-assisted clinical auditing system that reviews structured patient records to identify potential diagnostic blind spots, medication safety concerns, and changes in clinical measurements over time.

The project combines Python, Large Language Model (LLM) inference, structured patient data, and the Model Context Protocol (MCP) to expose clinical analysis capabilities through callable tools.

> **Disclaimer:** This project is intended for educational and research purposes. It is not a medical device and must not be used as a substitute for professional medical judgment.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Available MCP Tools](#available-mcp-tools)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Synthetic Patient Dataset](#synthetic-patient-dataset)
- [Testing](#testing)
- [Current Limitations](#current-limitations)
- [Privacy and Safety](#privacy-and-safety)
- [Contributing](#contributing)
- [License](#license)

## Overview

Clinical records may contain symptoms, laboratory results, medication information, and historical observations that are difficult to evaluate together. An existing diagnosis may not fully explain the available evidence, and changes in clinical measurements can be overlooked.

Diagnostic Blind Spot Auditor explores how AI-assisted analysis can support a more systematic review of this information.

The system provides three analysis capabilities:

- **Diagnostic blind-spot auditing:** Reviews available clinical context for findings that may warrant further investigation.
- **Medication safety review:** Examines listed medications for potential interactions and other safety concerns represented in the supplied record.
- **Clinical trend analysis:** Reviews laboratory results and visit notes to identify patterns that may indicate changes in a patient's condition.

The application assembles patient context and sends analysis prompts to a configured LLM through Hugging Face inference. Its output consists of potential findings that require independent review, not confirmed diagnoses or validated clinical recommendations.

## Key Features

### 1. Diagnostic Blind-Spot Auditing

Reviews the current diagnosis alongside available symptoms, laboratory results, medications, and visit notes.

The objective is to identify inconsistencies or overlooked possibilities that may merit additional clinical evaluation.

### 2. Medication Safety Review

Prepares a medication-focused analysis using the selected patient's record. The review can consider:

- Recorded medications and dosages.
- Potential drug–drug interactions.
- Possible medication-allergy conflicts when relevant information is available.
- Other safety concerns suggested by the supplied clinical context.

Results depend on the completeness of the record and the underlying model. They are not a replacement for a pharmacist's or clinician's review.

### 3. Clinical Trend Analysis

Examines recorded laboratory results and visit notes to summarize possible patterns over time.

The analysis can consider measurements such as ferritin and TSH when those values are present in the patient context. The current implementation does not independently validate clinical reference ranges or establish a medical diagnosis.

### 4. Model Context Protocol Integration

Uses FastMCP to expose clinical analysis functions as tools that compatible MCP clients can discover and invoke.

This allows the analysis functionality to be accessed through an MCP-compatible application rather than only through the standalone Python entry point.

### 5. Synthetic Patient Records

Includes five local JSON patient records representing different clinical scenarios. These records provide a repeatable data source for development and experimentation without requiring a live clinical database for the default workflow.

## System Architecture

The application is organized into three primary layers:

```text
              MCP Client / AI Assistant
                        |
                        v
                   server.py
                  FastMCP Server
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
     Diagnostic     Medication     Clinical
       Audit          Safety        Trends
          |             |             |
          +-------------+-------------+
                        |
                        v
                  fhir/client.py
              Patient Context Loading
                        |
                        v
                Synthetic JSON Records
                        |
                        v
                  llm/auditor.py
               Clinical Context Builder
                        |
                        v
              Hugging Face Inference API
              Meta-Llama-3-8B-Instruct
                        |
                        v
                 Analysis Response
```

### Component Responsibilities

| Component | Responsibility |
|---|---|
| `main.py` | Runs the standalone diagnostic auditing workflow. |
| `server.py` | Registers and exposes the three MCP tools. |
| `fhir/client.py` | Loads patient summaries from local synthetic JSON files by default. |
| `llm/auditor.py` | Builds clinical context, constructs analysis prompts, and calls Hugging Face inference. |
| `data/` | Stores the synthetic patient records. |
| `tests/` | Contains scripts intended to exercise the analysis workflow. |

The default workflow uses synthetic records. Although the FHIR client defines a HAPI FHIR base URL, the current non-synthetic path returns placeholder data rather than performing a live FHIR query.

## Available MCP Tools

The MCP server registers the following tools:

| Tool | Input | Purpose |
|---|---|---|
| `audit_blind_spots` | `patient_id` | Reviews clinical context for potential diagnostic blind spots. |
| `check_med_safety` | `patient_id` | Requests a medication safety review based on the patient record. |
| `analyze_trends` | `patient_id` | Analyzes laboratory results and visit notes for possible clinical trends. |

Each tool accepts a patient identifier as a string. If no identifier is supplied, the server defaults to `patient-001`.

Example identifiers:

```text
patient-001
patient-002
patient-003
patient-004
patient-005
```

These tools return text produced by the application, including error messages when an operation fails. They do not guarantee that every potential issue will be detected.

## Technology Stack

| Technology | Role |
|---|---|
| Python | Application logic and orchestration |
| Model Context Protocol (MCP) | Tool interface for compatible clients |
| FastMCP | MCP server and tool registration |
| Hugging Face Hub | LLM inference client |
| Meta-Llama-3-8B-Instruct | Configured language model |
| Python Dotenv | Environment variable loading |
| Requests | HTTP client dependency |
| JSON | Local synthetic patient data storage |

## Project Structure

```text
blind-spot-auditor/
├── main.py
├── server.py
├── requirements.txt
├── README.md
├── LICENSE
├── data/
│   ├── synthetic_patient.json
│   ├── patient_2_celiac.json
│   ├── patient_3_sleep_apnea.json
│   ├── patient_4_parkinsons.json
│   └── patient_5_lupus.json
├── fhir/
│   ├── __init__.py
│   └── client.py
├── llm/
│   ├── __init__.py
│   └── auditor.py
└── tests/
    ├── test_all_patients.py
    └── test_run.py
```

## Installation

### Prerequisites

- Python installed and available from the terminal.
- Git.
- A Hugging Face account and API token with the required inference access.
- An MCP-compatible client if you want to use the server tools.

The repository does not currently specify a tested minimum Python version. Use a Python version compatible with the installed dependencies and verify compatibility in your environment.

### 1. Clone the Repository

```bash
git clone https://github.com/krishbisen/blind-spot-auditor.git
cd blind-spot-auditor
```

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux or macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the repository root:

```dotenv
HF_API_KEY=your_hugging_face_api_token
```

Replace the example value with your own Hugging Face token.

The application loads this variable through `python-dotenv` and uses it to initialize the Hugging Face inference client in `llm/auditor.py`.

The configured model is:

```text
meta-llama/Meta-Llama-3-8B-Instruct
```

Successful inference depends on model availability, account permissions, network connectivity, and provider-side requirements.

**Security considerations:**

- Never commit your `.env` file or API token.
- Do not place API tokens directly in source code.
- If a token is exposed, revoke it and create a replacement.
- Ensure that data sent to an external inference provider is appropriate for the provider's terms and your privacy requirements.

## Usage

### 1. Run the Standalone Auditor

```bash
python main.py
```

The script loads `patient-001` from the local synthetic dataset, prepares the patient summary, requests a diagnostic blind-spot audit, and prints the returned report.

The patient identifier is currently specified in `main.py`. To run another synthetic case through this entry point, change the identifier passed to `run_audit()`.

### 2. Start the MCP Server

```bash
python server.py
```

The server registers the three tools described in [Available MCP Tools](#available-mcp-tools).

The current implementation uses:

```python
mcp.run(transport="sse")
```

This configures Server-Sent Events (SSE) transport. The connection address and client compatibility depend on the MCP library version and runtime configuration.

Configure your MCP client according to its supported transport and connection settings. Do not assume every client supports the same transport.

### 3. Invoke an MCP Tool

After connecting a compatible MCP client to the server, invoke one of the following operations.

**Diagnostic audit**

```text
Tool: audit_blind_spots
Arguments:
  patient_id: patient-001
```

**Medication safety review**

```text
Tool: check_med_safety
Arguments:
  patient_id: patient-002
```

**Clinical trend analysis**

```text
Tool: analyze_trends
Arguments:
  patient_id: patient-003
```

These are illustrative tool calls. The exact invocation procedure depends on the MCP client being used.

## Synthetic Patient Dataset

The `data/` directory contains five synthetic patient records.

| Identifier | Dataset file | Scenario represented |
|---|---|---|
| `patient-001` | `synthetic_patient.json` | Depression diagnosis with a potential hypothyroidism blind spot |
| `patient-002` | `patient_2_celiac.json` | IBS diagnosis with a potential celiac disease blind spot |
| `patient-003` | `patient_3_sleep_apnea.json` | Depression diagnosis with a potential sleep apnea blind spot |
| `patient-004` | `patient_4_parkinsons.json` | Anxiety diagnosis with a potential Parkinson's disease blind spot |
| `patient-005` | `patient_5_lupus.json` | Fibromyalgia diagnosis with a potential lupus blind spot |

These scenarios describe the intended themes of the supplied records. They do not demonstrate that the model consistently detects the corresponding conditions or that any condition is clinically confirmed.

The default client maps these identifiers to local JSON files and falls back to the first synthetic record when a file is missing. Invalid identifiers can therefore lead to analysis of the default record instead of the requested case.

## Testing

The repository contains scripts intended to exercise the analysis workflow. Their current compatibility should be verified before relying on them.

### Multi-Patient Script

```bash
python tests/test_all_patients.py
```

This script is intended to exercise the five patient scenarios and compare generated reports against expected blind-spot terms.

**Known issue:** The current script imports `run_diagnostic_audit` from `llm.auditor`, but that function is not defined in the current module. The script may therefore fail before running the checks. Resolve this mismatch before treating the script as a working test.

### Individual Test Script

```bash
python tests/test_run.py
```

This command runs the individual test script included in the repository. Its behavior and compatibility should be checked against the current source.

Testing may require a valid inference API token and access to the configured model. Results can vary with model responses and external service availability.

## Current Limitations

The following limitations should be considered when evaluating the current implementation:

- **Synthetic data by default:** Patient summaries are loaded from local JSON files.
- **Live FHIR integration is incomplete:** The non-synthetic code path currently returns placeholder data and does not implement a live patient query.
- **LLM-dependent results:** Findings are generated by a language model and may be incomplete, incorrect, or inconsistent.
- **No clinical validation claim:** The project does not establish diagnostic accuracy, sensitivity, specificity, or clinical safety.
- **Test compatibility issues:** The multi-patient script references a function that is not defined in the current auditor module.
- **External service dependency:** Analysis requires access to the configured Hugging Face inference service.
- **Patient selection fallback:** Unknown identifiers can fall back to the default synthetic record.

These limitations should be addressed before considering use in a real clinical environment.

## Privacy and Safety

The default workflow uses synthetic JSON records. The application constructs a clinical text summary before sending it to Hugging Face for inference.

The current implementation should not be described as fully local or as guaranteeing anonymization. The context builder includes fields such as patient name, age, gender, diagnosis, medications, laboratory values, and visit notes when available.

For responsible experimentation:

- Use synthetic or appropriately de-identified data.
- Do not submit identifiable patient information to an external service without the necessary authorization and privacy safeguards.
- Review the inference provider's data-handling policies before use.
- Treat model-generated findings as suggestions requiring independent verification.
- Do not use the application to make autonomous medical decisions.

## Contributing

Contributions that improve correctness, maintainability, testing, documentation, and safety are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make focused changes.
4. Add or update tests where appropriate.
5. Document relevant limitations and configuration changes.
6. Submit a pull request describing the changes.

## License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for the complete license terms.

## Disclaimer

Diagnostic Blind Spot Auditor is an educational and research project for exploring AI-assisted review of structured clinical information.

It is not intended to diagnose, treat, cure, or prevent any disease. Its outputs are not medical advice and must not replace evaluation by qualified healthcare professionals. Never delay or disregard professional medical advice based on an AI-generated report.