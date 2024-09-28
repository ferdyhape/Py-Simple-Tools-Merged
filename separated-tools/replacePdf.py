import os
from PyPDF2 import PdfReader, PdfWriter

def replace_pdf_page(input_pdf, replacement_pdf, page_num_to_replace):
    # Read the input PDF and the replacement PDF
    input_reader = PdfReader(input_pdf)
    replacement_reader = PdfReader(replacement_pdf)
    
    # Check if the requested page is within the valid range
    total_pages = len(input_reader.pages)
    if page_num_to_replace < 1 or page_num_to_replace > total_pages:
        print(f"Halaman {page_num_to_replace} tidak valid, hanya ada {total_pages} halaman.")
        return

    # Create a writer object for the output PDF
    writer = PdfWriter()

    # Add pages from the input PDF to the writer
    for i in range(total_pages):
        if i == page_num_to_replace - 1:  # Replace the desired page
            # Add the page from the replacement PDF
            writer.add_page(replacement_reader.pages[0])
        else:
            # Add the original page from the input PDF
            writer.add_page(input_reader.pages[i])

    # Extract the base name for naming
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]

    # Ensure the 'result/replace-pdf' directory exists
    output_dir = os.path.join("result", "replace-pdf")
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Define the output PDF name
    output_pdf = os.path.join(output_dir, f"{base_name}-replaced.pdf")

    # Save the output PDF to the 'result/replace-pdf' folder
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

    print(f"Halaman {page_num_to_replace} telah diganti. File disimpan di {output_pdf}")

# Usage with dynamic input
input_pdf = input("Masukkan nama file PDF asli: ").strip().strip("'\"")
replacement_pdf = input("Masukkan nama file PDF pengganti: ").strip().strip("'\"")
page_num_to_replace = int(input("Masukkan nomor halaman yang ingin diganti: "))

replace_pdf_page(input_pdf, replacement_pdf, page_num_to_replace)
