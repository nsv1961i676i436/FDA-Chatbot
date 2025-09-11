import fitz  # PyMuPDF
import re

TARGET_SECTIONS = [
    "INDICATIONS AND USAGE",
    "DOSAGE AND ADMINISTRATION",
    "WARNINGS AND PRECAUTIONS",
    "ADVERSE REACTIONS",
    "DRUG INTERACTIONS"
]

def extract_sections_from_pdf(pdf_file):
    pdf_file.seek(0)
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = doc[0].get_text()
    section_pattern = r"-{5,}(.*?)\-{5,}"
    matches = re.split(section_pattern, text)

    structured = {}
    for i in range(1, len(matches), 2):
        heading = matches[i].strip().upper()
        content = matches[i+1].strip()
        if heading in TARGET_SECTIONS:
            if heading in structured:
                structured[heading] += "\n\n" + content
            else:
                structured[heading] = content
    return structured
