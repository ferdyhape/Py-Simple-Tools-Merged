from datetime import datetime
import os
import zipfile
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from io import BytesIO
from PIL import Image

def replace_pdf_page(input_pdf, replacement_pdf, page_num_to_replace):
    input_reader = PdfReader(input_pdf)
    replacement_reader = PdfReader(replacement_pdf)

    total_pages = len(input_reader.pages)
    if page_num_to_replace < 1 or page_num_to_replace > total_pages:
        print(f"Page {page_num_to_replace} is invalid; there are only {total_pages} pages.")
        return

    writer = PdfWriter()
    for i in range(total_pages):
        if i == page_num_to_replace - 1:
            writer.add_page(replacement_reader.pages[0])
        else:
            writer.add_page(input_reader.pages[i])

    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    output_dir = os.path.join("result", "replace-pdf")
    os.makedirs(output_dir, exist_ok=True)

    output_pdf = os.path.join(output_dir, f"{base_name}-replaced.pdf")
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

    print(f"Page {page_num_to_replace} has been replaced. File saved at {output_pdf}")


def split_pdf(input_pdf):
    reader = PdfReader(input_pdf)
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    output_dir = os.path.join("result", "split-pdf")
    os.makedirs(output_dir, exist_ok=True)

    zip_file_path = os.path.join(output_dir, f"{base_name}-splitted.zip")
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for page_num in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])

            with BytesIO() as output_buffer:
                writer.write(output_buffer)
                zip_file.writestr(f"{base_name}-{page_num + 1}.pdf", output_buffer.getvalue())

    print(f"The PDF has been split and saved in ZIP at '{zip_file_path}'.")

def image_to_pdf(image_paths):
    output_dir = os.path.join("result", "image-to-pdf")
    os.makedirs(output_dir, exist_ok=True)

    # Get the current date and time for a unique ZIP file name
    date_str = datetime.now().strftime("Y%m%d%H%M%S") 
    zip_file_path = os.path.join(output_dir, f"{date_str}.zip")

    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for image_path in image_paths:
            try:
                image_input = Image.open(image_path)
                image_converted = image_input.convert('RGB')

                pdf_stream = BytesIO()
                image_converted.save(pdf_stream, format='PDF')
                pdf_stream.seek(0)

                # Use the original filename for the PDF name (without extension)
                original_base_name = os.path.splitext(os.path.basename(image_path))[0]
                pdf_file_name = f"{original_base_name}.pdf"
                
                zip_file.writestr(pdf_file_name, pdf_stream.read())
                print(f'-- Converted {image_path} to {pdf_file_name} and added to ZIP.')

            except Exception as e:
                print(f'Error converting {image_path}: {e}')

    print(f'-- All PDFs saved successfully in ZIP at {zip_file_path}.')

def merge_pdfs(pdf_files):
    output_dir = os.path.join("result", "merge-pdf")
    os.makedirs(output_dir, exist_ok=True)

    # Create a merger object
    merger = PdfMerger()

    # Append each PDF file to the merger
    for pdf_file in pdf_files:
        try:
            merger.append(pdf_file)  # Append the PDF file directly
        except Exception as e:
            print(f"Error adding {pdf_file}: {e}")

    if pdf_files:  # Check if there are any files
        name = input('Input name for merged PDF (without .pdf): ').strip()
        merged_pdf_path = os.path.join(output_dir, f"{name}-merged.pdf")

        # Write the merged PDF to the file
        merger.write(merged_pdf_path)
        merger.close()
        print(f'Merged PDF saved at {merged_pdf_path}')


def main():
    print("Select the tool you want to use:")
    print("1. Replace PDF Page")
    print("2. Split PDF")
    print("3. Image to PDF")
    print("4. Merge PDFs")
    
    choice = input("Enter your choice (1/2/3/4): ").strip()
    
    if choice == '1':
        input_pdf = input("Drag and drop the main PDF file into the terminal: ").strip().strip("'\"")
        replacement_pdf = input("Drag and drop the replacement PDF file into the terminal: ").strip().strip("'\"")
        page_num_to_replace = int(input("Enter the page number to replace: "))
        replace_pdf_page(input_pdf, replacement_pdf, page_num_to_replace)

    elif choice == '2':
        input_pdf = input("Drag and drop the PDF file to split into the terminal: ").strip().strip("'\"")
        split_pdf(input_pdf)

    elif choice == '3':
        image_paths = input('Drag and drop image paths into terminal (separated by commas if multiple): ').strip().split(',')
        image_paths = [path.strip().strip("'\"") for path in image_paths]
        image_to_pdf(image_paths)

    elif choice == '4':
        pdf_files = input('Drag and drop PDF paths into terminal (separated by commas if multiple): ').strip().split(',')
        pdf_files = [path.strip().strip("'\"") for path in pdf_files]
        merge_pdfs(pdf_files)

    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
