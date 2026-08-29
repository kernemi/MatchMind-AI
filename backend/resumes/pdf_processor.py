import fitz  # PyMuPDF
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_obj):
    """
    Extract text from a PDF file using PyMuPDF.
    
    Args:
        file_obj: A Django File object or file-like object containing PDF data
        
    Returns:
        str: Extracted text from the PDF
        
    Raises:
        ValidationError: If the file is not a valid PDF or extraction fails
    """
    try:
        # Read the file content
        file_content = file_obj.read()
        
        # Reset file pointer so it can be saved by Django
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
            
        # Open the PDF using fitz (PyMuPDF) from memory
        doc = fitz.open(stream=file_content, filetype="pdf")
        
        extracted_text = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            if text:
                extracted_text.append(text)
                
        doc.close()
        
        full_text = "\n".join(extracted_text)
        
        if not full_text.strip():
            raise ValidationError("Could not extract any text from the PDF. It might be an image-based PDF or encrypted.")
            
        return full_text
        
    except fitz.FileDataError:
        logger.error("Invalid PDF file provided")
        raise ValidationError("The provided file is not a valid PDF.")
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        if isinstance(e, ValidationError):
            raise
        raise ValidationError(f"Failed to process PDF: {str(e)}")
