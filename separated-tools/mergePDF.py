import os
from PyPDF2 import PdfMerger

print("-----------------------------------------\nPYTHON SCRIPT MERGE PDF - BY FERDYHAPE\n-----------------------------------------\n")

print("HOW to use this tool?\n-----------------------------------------\n"
      "1. Prepare PDF files in a local directory (make sure the PDF file names do not contain spaces, e.g., file1.pdf, file2.pdf)\n"
      "2. The merged PDF will be stored in 'result/merge-pdf'.\n"
      "3. Run the script code.\n"
      "4. If asked to input the PDF paths, directly drag and drop the PDF files to the terminal.\n"
      "5. Enter the file name (without .pdf) for the merged PDF.")

# Ensure the output directory exists
output_dir = os.path.join("result", "merge-pdf")
os.makedirs(output_dir, exist_ok=True)

while True:
    print('\n-----------------------------------------')
    pdf_files = []
    
    # Collecting PDF files
    while True:
        input_path = input("Input PDF path: ").strip().strip("'\"")
        pdf_files.append(input_path)
        if input('Do you want to insert another PDF? (Y/N) ').lower() != 'y':
            break

    # Create a merger object
    merger = PdfMerger()

    # Append each PDF file to the merger
    for pdf_file in pdf_files:
        try:
            merger.append(pdf_file)  # Append the PDF file directly
        except Exception as e:
            print(f"Error adding {pdf_file}: {e}")

    # Use the base name of the first PDF file as the merged name
    if pdf_files:  # Check if there are any files
        name = input('Input name for merged pdf (without .pdf): ')
        merged_pdf_path = os.path.join(output_dir, f"{name}.pdf")

        # Write the merged PDF to the file
        merger.write(merged_pdf_path)
        merger.close()
        print(f'Merged PDF saved at {merged_pdf_path}')

    if input('Do you want to merge PDFs again? (Y/N) ').lower() != 'y':
        break
