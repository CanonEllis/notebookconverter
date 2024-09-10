import streamlit as st
from nbconvert import PDFExporter
import nbformat
from io import BytesIO
import time  # To simulate loading time

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
    # Initialize the progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Read uploaded notebook
    status_text.text("Reading notebook...")
    notebook_content = uploaded_file.read().decode("utf-8")
    progress_bar.progress(25)  # Update progress to 25%
    
    # Step 2: Convert notebook to PDF
    status_text.text("Converting notebook to PDF...")
    try:
        time.sleep(1)  # Simulating some delay for each step (optional)
        pdf_bytes = convert_notebook_to_pdf(notebook_content)
        progress_bar.progress(75)  # Update progress to 75%
        
        # Step 3: Finalizing and showing the download button
        status_text.text("Finalizing conversion...")
        time.sleep(1)  # Simulating final delay
        progress_bar.progress(100)  # Update progress to 100%
        
        # Show success message
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
    finally:
        # Clear progress bar and status after completion
        progress_bar.empty()
        status_text.empty()
