# ASCHMA Dashboard Web Application

This web app provides a local dashboard for Adamawa State Contributory Health Management Agency (ASCHMA) to:

- View summary statistics
- Transfer enrollees between providers
- Generate enrollee ID cards (with dependants)
- Download lists of enrollees per health facility

## 🔧 Requirements

- Python 3.7+
- pip (Python package manager)

## 📦 Installation

```bash
# 1. Clone or unzip the folder
cd aschma_dashboard_app

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install required packages
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Access the app at http://localhost:5000

## 📝 Notes

- Policy number format: YLS/0079924/23/C/1
  - YLS: LGA code (e.g., Yola South)
  - 0079924: Unique ID for family unit
  - Final digit: 0 (principal), 1 (spouse), 2+ (children)
