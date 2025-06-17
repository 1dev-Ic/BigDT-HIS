import pandas as pd
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def clean_data(df):
    """Clean and standardize the dataframe"""
    df = df.astype(str)
    df['Dpndt.'] = df['Dpndt.'].str.strip()
    numeric_cols = ['Age', 'S/N']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df['Policy Number'] = df['Policy Number'].str.strip()
    return df

def get_family_members(df, unique_id):
    """Get family members with proper string comparison"""
    return df[df['Policy Number'].str.contains(f'/{unique_id}/', na=False)]

def generate_id_card(family_df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A5)
    width, height = A5
    
    # Organizational colors
    PRIMARY_COLOR = colors.HexColor('#2E7D32')  # Dark green
    TEXT_COLOR = colors.white
    
    # Set background
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    # Logo positioning - centered
    logo_y = height - 3.5*cm
    try:
        # Calculate center position for logos
        logo_spacing = 0.5*cm
        total_logo_width = 4*cm + logo_spacing  # 2cm each + spacing
        
        # Left logo (Adamawa)
        logo_left = Image("img/adamawa.png", width=2*cm, height=2*cm)
        logo_left.drawOn(c, (width - total_logo_width)/2, logo_y)
        
        # Right logo (ASCHMA)
        logo_right = Image("img/aschma.png", width=2*cm, height=2*cm)
        logo_right.drawOn(c, (width - total_logo_width)/2 + 2*cm + logo_spacing, logo_y)
    except:
        pass  # Skip logos if files not found
    
    # Header with green background - below logos
    header_y = logo_y - 3*cm  # Position header 3cm below logos
    header_height = 1.5*cm     # Reduced header height
    c.setFillColor(PRIMARY_COLOR)
    c.rect(0, header_y, width, header_height, fill=True, stroke=False)

    # Split header text into two lines
    c.setFont("Helvetica-Bold", 14)  # Slightly smaller font size
    c.setFillColor(TEXT_COLOR)
    line1 = "ADAMAWA STATE"
    line2 = "Contributory Health Management Agency"

    # Calculate text positions to fit within header
    text_y = header_y + (header_height/2)  # Vertical center of header
    line_spacing = 0.5*cm  # Reduced spacing between lines

    # Draw both lines centered within header
    c.drawCentredString(width/2, text_y + (line_spacing/2), line1)
    c.drawCentredString(width/2, text_y - (line_spacing/2), line2)
    
    # Set up styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=PRIMARY_COLOR,
        spaceAfter=12
    )
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['Normal'],
        backColor=PRIMARY_COLOR,
        textColor=TEXT_COLOR,
        fontSize=10,
        leading=14
    )
    
    # Find principal (dependent_id = 0)
    principal = None
    for _, row in family_df.iterrows():
        policy_parts = row['Policy Number'].split('/')
        if len(policy_parts) >= 5 and policy_parts[4] == '0':
            principal = row
            break
    
    if principal is not None:
        # Principal information section
        y_position = header_y - 1.5*cm
        
        # ID Card title
        title = Paragraph("<b>ENROLLEE ID CARD</b>", title_style)
        title.wrapOn(c, width-2*cm, 2*cm)
        title.drawOn(c, 1*cm, y_position)
        y_position -= 1.5*cm
        
        # Principal details
        details = [
            f"<b>Principal Officer:</b> {principal['Name']}",
            f"<b>Policy Number:</b> {principal['Policy Number']}",
            f"<b>Facility:</b> <font color='{PRIMARY_COLOR.hexval()}'><b>{principal['Provider']}</b></font>",
            f"<b>Family ID:</b> {principal['Policy Number'].split('/')[1]}"
        ]
        
        for detail in details:
            p = Paragraph(detail, styles['Normal'])
            p.wrapOn(c, width-2*cm, 1*cm)
            p.drawOn(c, 1*cm, y_position)
            y_position -= 0.7*cm
        
        # MDA/LGA with highlight
        mda_text = f"<b>MDA/LGA:</b> {principal.get('MDA/LGA', 'N/A')}"
        mda_para = Paragraph(mda_text, highlight_style)
        mda_para.wrapOn(c, width-2*cm, 0.7*cm)
        mda_para.drawOn(c, 1*cm, y_position)
        y_position -= 1.2*cm
    
    # Dependents table
    if len(family_df) > 1:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(PRIMARY_COLOR)
        c.drawString(1*cm, y_position, "DEPENDENTS:")
        y_position -= 0.5*cm
        
        # Prepare table data
        data = [['Name', 'Age', 'Gender', 'Relationship']]
        
        for _, row in family_df.iterrows():
            policy_parts = row['Policy Number'].split('/')
            if len(policy_parts) >= 5 and policy_parts[4] != '0':
                relationship = {
                    '1': 'Spouse',
                    '2': 'Child',
                    '3': 'Child',
                    '4': 'Child',
                    '5': 'Child'
                }.get(policy_parts[4], 'Dependent')
                data.append([
                    row['Name'],
                    str(row.get('Age', 'N/A')),
                    row.get('Gender', 'N/A'),
                    relationship
                ])
        
        if len(data) > 1:
            table = Table(data, colWidths=[5*cm, 2*cm, 2*cm, 3*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, 0), TEXT_COLOR),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ]))
            
            table.wrapOn(c, width-2*cm, height)
            table.drawOn(c, 1*cm, y_position - (0.5*cm * len(data)))
    
    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(width/2, 1*cm, 
                       "This ID is valid when presented with a valid government-issued photo ID")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()