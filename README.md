# Diagnostic Blind Spot Auditor

A clinical AI agent that identifies overlooked medical conditions by "red-teaming" patient diagnoses. Built for the Agents Assemble Hackathon 2026.

## What It Does

This tool connects to FHIR patient data, feeds it to a Large Language Model (LLM), and generates reports highlighting potential diagnostic blind spots — things doctors might be missing. It acts as a second opinion AI that asks: "What is everyone assuming is correct that might actually be wrong?"


##  How it Works
This agent operates as a local-first clinical auditor. By using the **Model Context Protocol (MCP)**, it ensures that sensitive patient data is processed locally via the `fhir/client.py` and only anonymized clinical context is sent to the Hugging Face Inference API for auditing. This architecture prioritizes patient privacy while leveraging state-of-the-art LLMs.

## Features

- **Diagnostic Blind Spot Audit**: Red-teams current diagnosis using full clinical history to find inconsistencies.
- **Medication Safety Check**: Automatically flags drug-drug clashes and allergy contraindications.
- **Clinical Trend Analysis**:Deciphers longitudinal lab data (TSH, Ferritin, etc.) to detect progressive declines.
- **FHIR Integration**: Connects to public FHIR servers for patient data
- **MCP Server**: Exposes tools via Model Context Protocol for integration with AI assistants
- **Multi-Patient Testing**: Includes 5 diverse patient cases for validation

## Project Structure

```
blind-spot-auditor/
├── main.py                 # Entry point script
├── server.py               # MCP server for tool exposure
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── data/                   # Patient data files
│   ├── synthetic_patient.json
│   ├── patient_2_celiac.json
│   ├── patient_3_sleep_apnea.json
│   ├── patient_4_parkinsons.json
│   └── patient_5_lupus.json
├── fhir/                   # FHIR client module
│   ├── __init__.py
│   ├── client.py           # FHIR data fetching
│   └── __pycache__/
├── llm/                    # LLM auditing module
│   ├── __init__.py
│   ├── auditor.py          # AI analysis tools
│   └── __pycache__/
└── tests/                  # Test scripts
    ├── test_all_patients.py
    └── test_run.py
```

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd blind-spot-auditor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Hugging Face API key:
     ```
     HF_API_KEY=your_hugging_face_api_key_here
     ```

##  Available MCP Tools
When connected to an AI assistant, this server exposes:
1. `audit_blind_spots(patient_id)`: Analyzes records for misdiagnoses.
2. `check_med_safety(patient_id)`: Performs real-time medication safety checks.
3. `analyze_trends(patient_id)`: Provides a chronological summary of lab improvements or declines.

## Usage

### Running the Main Script

Execute the diagnostic audit on the synthetic patient:

```bash
python main.py
```

This will:
1. Load patient data from FHIR/synthetic source
2. Run the blind spot audit using the LLM
3. Display a structured report

### Running the MCP Server

Start the server to expose tools for AI assistants:

```bash
python server.py
```

The server provides three tools:
- `audit_blind_spots`: Perform diagnostic blind spot audit
- `check_med_safety`: Check medication safety and interactions
- `analyze_trends`: Analyze clinical trends from lab results

### Testing Multiple Patients

Run the comprehensive test suite:

```bash
python tests/test_all_patients.py
```

This tests the auditor against 5 different patient cases covering various conditions.

## Dependencies

- `mcp`: Model Context Protocol for tool exposure
- `fastmcp`: Fast MCP server implementation
- `uvicorn`: ASGI server for the MCP endpoint
- `huggingface_hub`: Hugging Face API client
- `python-dotenv`: Environment variable management
- `requests`: HTTP client for FHIR API calls

## Configuration

The system uses Hugging Face's Meta-Llama-3-8B-Instruct model by default. You can modify the model in `llm/auditor.py` if needed.

For production use, consider switching to OpenAI or Anthropic APIs by updating the `run_diagnostic_audit` function in `llm/auditor.py`.

## Data Sources

- **Synthetic Data**: Local JSON files in the `data/` directory for testing
- **Live FHIR**: Public HAPI FHIR server (https://hapi.fhir.org/baseR4) for real patient data structure

## Hackathon Context

This project was developed for the Agents Assemble Hackathon 2026. It demonstrates:
- Integration of healthcare standards (FHIR)
- AI-powered clinical decision support
- Modular architecture for MCP integration
- Comprehensive testing across multiple medical scenarios

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Add appropriate license here]

## Disclaimer

This tool is for educational and research purposes only. It should not be used for actual medical diagnosis or treatment decisions. Always consult qualified healthcare professionals for medical advice.