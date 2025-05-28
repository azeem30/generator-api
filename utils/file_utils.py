import PyPDF2
import json

def parse_pdf_to_text(pdf_path):
    """Parses the PDF into text as a string"""
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
    except FileNotFoundError as fnfe:
        raise fnfe(f"PDF not found at: {pdf_path}")
    except PyPDF2.errors.PdfReadError as pre:
        raise pre(f"Invalid or corrupted PDF file")

def clean_text(text):
    try:
        cleaned_text = ""
        allowed_punctuations = [' ', '.', ',', '\n', '=', '/', '&', '|', "'", ':', ';', '-']
        for char in text:
            is_letter = 'a' <= char <= 'z' or 'A' <= char <= 'Z'
            is_number = '0' <= char <= '9'
            is_allowed_punctuation = char in allowed_punctuations
            if is_letter or is_number or is_allowed_punctuation:
                cleaned_text += char
        return cleaned_text
    except Exception as e:
        raise e()

def parse_string_to_json(string):
    """Parse the string passed as the argument into a JSON object"""
    try:
        json_object = json.loads(string)
        return json_object
    except Exception as e:
        raise e()
