import pytesseract
from PIL import Image
import os
import pdfplumber
from docx import Document
import sys

# Set the path to tesseract executable (Modify this path based on your OS and installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(file_path):
    try:
        with Image.open(file_path) as img:
            return pytesseract.image_to_string(img)
    except Exception as e:
        return f"Error extracting text from image: {e}"

def extract_text_from_pdf(file_path):
    try:
        text = ''
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text if text else "No text found in the PDF."
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error extracting text from DOCX: {e}"

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error extracting text from TXT: {e}"

def extract_text(folder_path, filename, date):
    try:
        # Combine folder path and filename to get the full file path
        file_path = os.path.join(folder_path, filename)

        # Determine the file type by extension
        file_ext = os.path.splitext(filename)[1].lower()
        file_base = os.path.splitext(filename)[0]  # Extract base filename

        if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            extracted_text = extract_text_from_image(file_path)
        elif file_ext == '.pdf':
            extracted_text = extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            extracted_text = extract_text_from_docx(file_path)
        elif file_ext == '.txt':
            extracted_text = extract_text_from_txt(file_path)
        else:
            return f"Unsupported file type: {file_ext}"

        # Save the extracted text to a text file with the same base filename and appended date
        output_filename = os.path.join(folder_path, f"{file_base}_{date}.txt")
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(extracted_text)

        return f"Text successfully extracted and saved to {output_filename}"

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Get arguments from command-line
    folder_path = sys.argv[1]
    filename = sys.argv[2]
    date = sys.argv[3]

    result = extract_text(folder_path, filename, date)
    print(result)
