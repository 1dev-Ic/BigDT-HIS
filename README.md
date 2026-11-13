# BigDT HIS — ASCHMA Enrollee Dashboard

BigDT HIS is a lightweight web dashboard developed to help the Adamawa State Contributory Health Management Agency (ASCHMA) work with health enrollee records. It was used by the agency for a short period in 2025 while its institutional server was experiencing a major outage, providing a temporary local way to view and manage enrollee data.

The application reads enrollee records from a CSV file and provides facility-level summaries and practical enrollee administration tools.

## Features

- Show total enrollee counts and the facilities represented in the dashboard.
- Transfer a policy holder’s family group to another listed provider.
- Generate a PDF ID card for an enrollee family, including dependants.
- Download an enrollee list for a selected provider as a CSV file.

## Technology

- Python and Flask
- Pandas for CSV data handling
- ReportLab for PDF ID-card generation
- HTML templates under `templates/`

## Data source

By default, the application reads `aschma_sample_data.csv` from the project directory. Provider names are configured in `app.py`. For a different dataset or provider list, review and update the corresponding application configuration and confirm that the CSV column names and policy-number format match the code.

## Run locally

Python 3 and `pip` are required.

```bash
# Clone the repository and enter its directory
cd BigDT-HIS

# Create and activate a virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the local development server
python app.py
```

Then open <http://127.0.0.1:5000> in a browser on the same computer.

## Project history and status

BigDT HIS was a short-term operational tool used during the agency server outage in 2025. It was intended to support continuity of enrollee administration while the institutional system was unavailable. It is a separate application from BigDT, the mobile LGA health-facility data collection and reporting tool.

## Deployment and data protection

The repository is configured for local development and should not be exposed directly as a public production service. Before any deployment with live enrollee information, review access controls, data protection requirements, application secrets, file handling, and Flask’s development-server settings. Do not commit real enrollee or other confidential health data to a public repository.

## Acknowledgement

Developed for the Adamawa State Contributory Health Management Agency (ASCHMA).
