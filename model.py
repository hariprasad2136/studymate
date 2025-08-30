# model.py
import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from a PDF file uploaded via Streamlit.
    """
    try:
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Error reading PDF: {e}")
