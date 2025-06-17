from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import pandas as pd
from werkzeug.utils import secure_filename
import os
from utils import generate_id_card, get_family_members, clean_data

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
DATA_FILE = 'aschma_sample_data.csv'

def get_providers_list():
    """Return pre-parsed list of unique providers matching CSV data"""
    try:
        # Pre-parsed list of providers from your CSV data
        providers = [
            "MEDDY HOSPITAL LIMITED",
            "COTTAGE HOSPITAL MAYO-BELWA",
            "NEW BOSHANG",
            "SPECIALIST HOSPITAL YOLA",
            "General Hospital Ganye",
            "COTTAGE HOSPITAL HONG",
            "GENERAL HOSPITAL MICHIKA",
            "GENERAL HOSPITAL MUBI",
            "ABSOLUTE CARE CONSULTANTS CLINIC",
            "AISHA CLINIC",
            "DAAMA SPECIALIST HOSPITAL",
            "PEACE HOSPITAL",
            "ADAMAWA HOSPITAL LIMITED",
            "COTTAGE HOSPITAL GUYUK",
            "TRUST MEDICAL CENTRE",
            "BASIRA CLINIC AND MATERNITY",
            "BAMAIYI HOSPITAL",
            "General Hospital Numan"
        ]
        
        # Maintain same sorting behavior as original
        return sorted(providers)
        
    except Exception as e:
        print(f"Error loading providers: {e}")
        return []
def get_enrollee_count():
    """Get total number of enrollees"""
    try:
        df = pd.read_csv(DATA_FILE)
        return len(df)
    except:
        return 0

@app.route('/')
def index():
    providers = get_providers_list()
    summary = {
        'total_enrollees': get_enrollee_count(),
        'unique_facilities': len(providers),
        'providers': providers
    }
    return render_template('index.html', summary=summary)

@app.route('/transfer', methods=['POST'])
def transfer():
    try:
        policy = request.form['policy']
        new_provider = request.form['new_provider']
        
        # Validate provider exists
        providers = get_providers_list()
        if new_provider not in providers:
            flash("Invalid provider selected", "danger")
            return redirect(url_for('index'))
        
        # Read and clean data
        df = clean_data(pd.read_csv(DATA_FILE))
        
        # Check if policy exists
        if policy not in df['Policy Number'].values:
            flash("Policy number not found", "danger")
            return redirect(url_for('index'))
            
        # Update provider (including family members)
        unique_id = policy.split('/')[1]
        df.loc[df['Policy Number'].str.contains(f'/{unique_id}/'), 'Provider'] = new_provider
        df.to_csv(DATA_FILE, index=False)
        
        flash(f"Successfully transferred family to {new_provider}", "success")
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Transfer failed: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.route('/download', methods=['GET'])
def download():
    provider = request.args.get('provider')
    providers = get_providers_list()
    
    if not provider or provider not in providers:
        flash("Please select a valid provider", "danger")
        return redirect(url_for('index'))
    
    try:
        df = clean_data(pd.read_csv(DATA_FILE))
        filtered = df[df['Provider'] == provider]
        
        if filtered.empty:
            flash("No enrollees found for selected provider", "warning")
            return redirect(url_for('index'))
            
        filename = f'enrollees_{secure_filename(provider)}.csv'
        filtered.to_csv(filename, index=False)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        flash(f"Download failed: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.route('/generate_id/<unique_id>')
def generate_id(unique_id):
    try:
        df = clean_data(pd.read_csv(DATA_FILE))
        family_df = get_family_members(df, unique_id)
        
        if family_df.empty:
            flash("No family members found with that ID", "danger")
            return redirect(url_for('index'))
        
        pdf_bytes = generate_id_card(family_df)
        
        # Clean up any old files
        for f in os.listdir():
            if f.endswith('_id_card.pdf'):
                try:
                    os.remove(f)
                except:
                    pass
        
        filename = f'{unique_id}_id_card.pdf'
        with open(filename, 'wb') as f:
            f.write(pdf_bytes)
        
        return send_file(
            filename,
            download_name=filename,
            as_attachment=True,
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f"ID card generation failed: {str(e)}", "danger")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)