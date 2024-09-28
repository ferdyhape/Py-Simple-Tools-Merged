import os
import zipfile
from io import BytesIO
from PIL import Image

print("-----------------------------------------\nPYTHON SCRIPT IMAGE TO PDF - BY FERDYHAPE\n-----------------------------------------\n")

print("HOW to use this tool?\n-----------------------------------------\n1. Prepare image files in a local directory (make sure the image file names do not contain spaces, e.g., file_image.jpg, fileimage.jpg)\n2. Prepare a local path folder for PDF storage (if you don't want to always include the local path folder, change the default save path in the code)\n3. Run the script code\n4. If asked to input the image path, directly drag and drop the image file to the terminal\n5. Enter the local path folder for storing PDF files (if you have changed the default, you just have to enter without inputting)\n6. Enter file name (without .pdf)")

# Ensure the output directory exists
output_dir = os.path.join("result", "image-to-pdf")
os.makedirs(output_dir, exist_ok=True)

# Input multiple images
image_paths = input('Input image paths (separated by commas): ').strip().split(',')
image_paths = [path.strip().strip("'\"") for path in image_paths]  # Clean up whitespace and quotes

# Use the first image name as the base for the PDF file
base_name = os.path.splitext(os.path.basename(image_paths[0]))[0]

# Prepare the ZIP file path
zip_file_path = os.path.join(output_dir, f"{base_name}.zip")

# Create a ZIP file to store PDFs
with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
    for image_path in image_paths:
        try:
            # Open and convert the image to RGB
            image_input = Image.open(image_path)
            image_converted = image_input.convert('RGB')

            # Create a BytesIO stream to hold the PDF in memory
            pdf_stream = BytesIO()
            image_converted.save(pdf_stream, format='PDF')
            pdf_stream.seek(0)  # Move to the beginning of the stream

            # Define the PDF file name
            pdf_file_name = f"{base_name}-{image_paths.index(image_path) + 1}.pdf"

            # Write the PDF to the ZIP file from the BytesIO stream
            zip_file.writestr(pdf_file_name, pdf_stream.read())
            print(f'-- Converted {image_path} to {pdf_file_name} and added to ZIP.')

        except Exception as e:
            print(f'Error converting {image_path}: {e}')

print(f'-- All PDFs saved successfully in ZIP at {zip_file_path}.')
