import os
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_barcode_pdf(input_file, output_pdf):
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Create a PDF canvas
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    y_position = height - 50  # Start position for entries in the PDF

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        code_value = str(row['A'])  # Assuming 'A' is the column name

        # Generate barcode and save as PNG
        barcode = Code128(code_value, writer=ImageWriter())
        barcode_filename = f"{code_value}.png"
        barcode.save(barcode_filename)
        
        # Draw text and barcode image on the PDF
        c.drawString(50, y_position, code_value)  # Text next to the barcode
        c.drawImage(barcode_filename, 150, y_position - 10, width=150, height=50)
        
        # Move to the next position
        y_position -= 100  # Adjust for spacing between entries
        
        # Clean up temporary barcode image
        os.remove(barcode_filename)
        
        # Start a new page if needed
        if y_position < 50:
            c.showPage()
            y_position = height - 50

    # Save the PDF file
    c.save()

if __name__ == "__main__":
    # Find the uploaded Excel file in the 'uploads' folder
    input_file = next(f for f in os.listdir("uploads") if f.endswith(".xlsx"))
    output_pdf = f"output/{input_file.replace('.xlsx', '.pdf')}"
    os.makedirs("output", exist_ok=True)  # Ensure output folder exists
    
    # Generate the PDF with barcodes
    generate_barcode_pdf(f"uploads/{input_file}", output_pdf)
