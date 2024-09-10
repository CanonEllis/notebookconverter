import streamlit as st
from nbconvert import PDFExporter
import nbformat
from io import BytesIO
import os

# Function to convert notebook to PDF including code blocks
def convert_notebook_to_pdf(notebook_content):
    # Read the notebook content using nbformat
    notebook = nbformat.reads(notebook_content, as_version=4)
    
    # Use PDFExporter to convert the notebook to PDF
    pdf_exporter = PDFExporter()
    
    # Ensure that input cells (code blocks) are included
    pdf_exporter.exclude_input = False  # Set this to False to include code cells
    pdf_exporter.exclude_output_prompt = False  # Include output prompts (optional)
    
    pdf_data, _ = pdf_exporter.from_notebook_node(notebook)
    
    # Return the PDF data as bytes
    return pdf_data

# Streamlit app UI
st.title("Jupyter Notebook to PDF Converter")

# File uploader for Jupyter Notebook files
uploaded_file = st.file_uploader("Upload a Jupyter Notebook (.ipynb)", type=["ipynb"])

if uploaded_file is not None:
    # Read uploaded notebook
    notebook_content = uploaded_file.read().decode("utf-8")
    
    # Convert notebook to PDF
    try:
        pdf_bytes = convert_notebook_to_pdf(notebook_content)
        
        # Download button for the converted PDF
        st.success("Notebook converted to PDF successfully!")
        
        # Create a download button
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="converted_notebook.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"An error occurred during conversion: {e}")
