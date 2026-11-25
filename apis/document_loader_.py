from pathlib import Path
# import fitz #ouutdated 
import pymupdf #new
from docx import Document as DocxDocument
from langchain_core.documents import Document

def load_pdf(file_path):
    documents = []
    # pdf = fitz.open(file_path)
    pdf = pymupdf.open(file_path)

    for page_number, page in enumerate(pdf):
        text = page.get_text("text").strip()
        if not text:
            continue
        document = Document(
            page_content=text,
            metadata={
                "source": str(Path(file_path).resolve()),
                "file_name": Path(file_path).name,
                "file_type": "pdf",
                "page": page_number + 1
            }
        )
        documents.append(document)
    pdf.close()
    return documents

def load_docx(file_path):

    doc = DocxDocument(file_path)

    content = []

        # Extract paragraphs
    for paragraph in doc.paragraphs:

        if paragraph.text.strip():
            content.append(paragraph.text)

    # Extract tables
    for table in doc.tables:

        for row in table.rows:

            row_text = " | ".join(
                cell.text.strip()
                for cell in row.cells
            )

            if row_text.strip():
                content.append(row_text)

    text = "\n".join(content)

    if not text.strip():
        return []

    document = Document(
        page_content=text,
        metadata={
            "source": str(Path(file_path).resolve()),
            "file_name": Path(file_path).name,
            "file_type": "docx"
        }
    )

    return [document]

def load_markdown(file_path):

    text = Path(file_path).read_text(
        encoding="utf-8"
    )

    if not text.strip():
        return []

    document = Document(
        page_content=text,
        metadata={
            "source": str(Path(file_path).resolve()),
            "file_name": Path(file_path).name,
            "file_type": "md"
        }
    )

    return [document]

def load_document(file_path):

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    elif extension == ".md":
        return load_markdown(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )