import pdfplumber
import base64

def extract_pdf_text(file_path):
    """
    Extract text from a PDF file using pdfplumber
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content
    """
    text_content = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text_content += extracted_text + "\n\n"
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    return text_content

def encode_file_to_base64(file_path):
    """
    Encode a file to base64 for storage in the database
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Base64 encoded file content
    """
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        return base64.b64encode(file_data).decode('utf-8')
    except Exception as e:
        raise Exception(f"Error encoding file to base64: {str(e)}")

def decode_base64_to_file(base64_data, output_path):
    """
    Decode base64 data and save to a file
    
    Args:
        base64_data (str): Base64 encoded file content
        output_path (str): Path to save the decoded file
        
    Returns:
        bool: True if successful
    """
    try:
        file_data = base64.b64decode(base64_data)
        with open(output_path, 'wb') as f:
            f.write(file_data)
        return True
    except Exception as e:
        raise Exception(f"Error decoding base64 data: {str(e)}")