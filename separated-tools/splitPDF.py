import os
import zipfile
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def split_pdf(input_pdf):
    # Read the input PDF
    reader = PdfReader(input_pdf)

    # Extract the base name (without extension) for naming
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]

    # Ensure the 'result/split' directory exists
    output_dir = os.path.join("result", "split")
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Create a ZIP file to store the split PDFs
    zip_file_path = os.path.join(output_dir, f"{base_name}.zip")
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        # Split the PDF and add each page to the ZIP
        for page_num in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])

            # Write the page to a bytes buffer
            with BytesIO() as output_buffer:
                writer.write(output_buffer)
                # Write the PDF from the buffer directly to the ZIP file
                zip_file.writestr(f"{base_name}-{page_num + 1}.pdf", output_buffer.getvalue())

    print(f"PDF berresult dibagi dan disimpan dalam ZIP di '{zip_file_path}'.")

# Usage with dynamic input
input_pdf = input("Masukkan nama file PDF yang ingin dibagi: ").strip().strip("'\"")
split_pdf(input_pdf)
