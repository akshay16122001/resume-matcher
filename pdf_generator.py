from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.colors import black, HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import re

def generate_pdf_resume(tailored_content, output_path="tailored_resume.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch
    )

    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    name_style = ParagraphStyle(
        'Name',
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=black,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    contact_style = ParagraphStyle(
        'Contact',
        fontName='Helvetica',
        fontSize=9,
        textColor=HexColor('#333333'),
        alignment=TA_CENTER,
        spaceAfter=8
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=black,
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9,
        textColor=HexColor('#1A1A1A'),
        alignment=TA_JUSTIFY,
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=9,
        textColor=HexColor('#1A1A1A'),
        alignment=TA_JUSTIFY,
        leftIndent=15,
        spaceAfter=3
    )

    job_header_style = ParagraphStyle(
        'JobHeader',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        textColor=black,
        spaceBefore=8,
        spaceAfter=3
    )

    # Parse and render content
    lines = tailored_content.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 3))
            continue

        # Name line
        if line.isupper() and len(line.split()) <= 4 and len(line) < 40:
            story.append(Paragraph(line.title(), name_style))

        # Contact info
        elif '@' in line or '(' in line or 'linkedin' in line.lower():
            story.append(Paragraph(line, contact_style))

        # Section headers
        elif line.endswith(':') and line.isupper():
            story.append(HRFlowable(width="100%", thickness=0.8, color=black, spaceAfter=3))
            story.append(Paragraph(line, section_header_style))

        # Job headers
        elif '|' in line and not line.startswith('•'):
            story.append(Paragraph(line, job_header_style))

        # Bullet points
        elif line.startswith('•') or line.startswith('-'):
            clean = line.lstrip('•-').strip()
            story.append(Paragraph(f"• {clean}", bullet_style))

        # Regular text
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
    return output_path