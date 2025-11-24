from pathlib import Path

def parse_text(file_path: str) -> str:
    """Parse text file."""
    return Path(file_path).read_text()

def parse_pdf(file_path: str) -> str:
    """Parse PDF file."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except ImportError:
        raise ImportError("pypdf required for PDF parsing: pip install pypdf")

def parse_file(file_path: str) -> str:
    """Parse file based on extension."""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext in [".txt", ".md", ".markdown"]:
        return parse_text(file_path)
    else:
        # Try as text
        return parse_text(file_path)

