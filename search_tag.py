import os
import pytesseract
from pdf2image import convert_from_path

def extract_text_from_file(file_path):
    """Extract text from images and PDFs."""
    try:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
            # Extract text using OCR for image files
            text = pytesseract.image_to_string(file_path)
        elif file_path.lower().endswith('.pdf'):
            # Convert PDF pages to images and extract text
            images = convert_from_path(file_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
        else:
            # Unsupported file format
            raise ValueError("Unsupported file format. Please use an image or PDF file.")

        if not text.strip():
            raise ValueError("No text could be extracted from the document.")
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from file: {e}")

def save_extracted_text(text, folder_path, filename, search_term):
    """Save the extracted text to a new file, tagging the search term."""
    try:
        # Tag the search term in the extracted text
        if search_term:
            tagged_text = text.replace(search_term, f"[[FOUND]]{search_term}[[/FOUND]]")
        else:
            tagged_text = text

        # Save as a new text file with the same base name
        base_filename = os.path.splitext(filename)[0]
        output_filename = os.path.join(folder_path, f"{base_filename}_extracted.txt")
        
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(tagged_text)
        
        print(f"Text successfully extracted and saved to {output_filename}")
        return output_filename
    except Exception as e:
        raise Exception(f"Error saving text: {e}")

def search_in_text_file(text_file_path, search_term):
    """Search for a specific term in the text file and notify the user."""
    try:
        with open(text_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if search_term in content:
            print(f"The term '{search_term}' was found in the text file.")
        else:
            print(f"The term '{search_term}' was NOT found in the text file.")
    except Exception as e:
        raise Exception(f"Error searching in text file: {e}")

def main():
    # Get folder path and filename from the user
    folder_path = input("Enter the folder path where the file is located: ")
    filename = input("Enter the file name (with extension): ")
    
    # Construct full file path
    file_path = os.path.join(folder_path, filename)

    # Extract text from the file
    try:
        extracted_text = extract_text_from_file(file_path)
        
        # Ask user for the term to search
        search_term = input("Enter the term to search for in the extracted text: ")
        
        # Save the extracted text and tag the search term
        text_file_path = save_extracted_text(extracted_text, folder_path, filename, search_term)

        # Search for the term and notify the user
        search_in_text_file(text_file_path, search_term)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

