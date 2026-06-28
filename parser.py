import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def clean_text(text):
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s\.,@\-\+\(\)\/]', '', text)
    # Strip leading/trailing spaces
    text = text.strip()
    return text

def parse_resume(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)
    return cleaned_text

if __name__ == "__main__":
    # Test the parser
    import sys
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        text = parse_resume(pdf_path)
        print("✅ Resume extracted successfully!")
        print(f"📄 Total characters: {len(text)}")
        print("\n--- FIRST 500 CHARACTERS ---")
        print(text[:500])
    else:
        print("Usage: python3 parser.py your_resume.pdf")