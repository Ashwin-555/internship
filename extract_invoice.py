import fitz  # PyMuPDF
import re

def extract_invoice_data(pdf_file):
    """Extract invoice number and date from a PDF file."""
    # Open the PDF file
    doc = fitz.open(pdf_file)
    
    invoice_number = None
    invoice_date = None

    # Iterate through pages in the document
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        # Regex for invoice number and date (adjust these based on the template)
        invoice_num_match = re.search(r'Invoice\s*#?\s*([A-Za-z0-9-]+)', text, re.IGNORECASE)  # Flexible pattern for invoice numbers
        invoice_date_match = re.search(r'Date:\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})', text, re.IGNORECASE)  # Flexible date format

        if invoice_num_match:
            invoice_number = invoice_num_match.group(1)
        
        if invoice_date_match:
            invoice_date = invoice_date_match.group(1)
        
        # If both values are found, we can exit early
        if invoice_number and invoice_date:
            break

    doc.close()
    
    return invoice_number, invoice_date

def main():
    pdf_path = input("Enter the path to the PDF file: ")
    invoice_number, invoice_date = extract_invoice_data(pdf_path)

    if invoice_number:
        print(f"Invoice Number: {invoice_number}")
    else:
        print("Invoice Number not found.")

    if invoice_date:
        print(f"Invoice Date: {invoice_date}")
    else:
        print("Invoice Date not found.")

if __name__ == "__main__":
    main()
