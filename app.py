import streamlit as st
import replicate
import os
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, PageBreak, KeepTogether
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from reportlab.graphics.shapes import Rect

# Function to create a blank page
def create_blank_page(page_size):
    blank_page = PageBreak()
    elements = [blank_page]
    doc = SimpleDocTemplate("blank_page.pdf", pagesize=page_size)
    doc.build(elements)
    with open("blank_page.pdf", "rb") as blank_file:
        blank_pdf = blank_file.read()
    return blank_pdf

# Set Replicate API token from Streamlit secrets
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.title("Coloring Book PDF Generator")

prompts = st.text_area("Enter your prompts (one per line):")

if st.button("Generate Coloring Book PDF"):
    # Split prompts into a list
    prompt_list = [prompt.strip() for prompt in prompts.split("\n") if prompt.strip()]

    # Run Replicate model on each prompt
    images = []
    for prompt in prompt_list:
        input = {
            "prompt": prompt,
            "negative_prompt": "complex, realistic, color, gradient, cropped, cut off, out of frame",  # Modified negative prompt
            "width": 1024,
            "height": 1024
        }
        output = replicate.run(
            "pnickolas1/sdxl-coloringbook:d2b110483fdce03119b21786d823f10bb3f5a7c49a7429da784c5017df096d33",
            input=input
        )
        image_url = output[0]  # Assuming the model returns a list with a single URL
        images.append(image_url)

    # Create a PDF file with the generated images
    doc = SimpleDocTemplate("coloring_book.pdf", pagesize=(8.5*inch, 11*inch))  # Set page size to 8.5 x 11 inches
    elements = []
    for image_url in images:
        response = requests.get(image_url)
        image_file = BytesIO(response.content)
        image = Image(image_file, 8*inch, 8*inch)  # Adjust image size if needed
        blank_page_data = create_blank_page((8.5*inch, 11*inch))

        # Add a solid line around the image
        rect = Rect(0, 0, 8*inch, 8*inch, strokeColor=black, strokeWidth=1)
        centered_elements = [KeepTogether([rect, image, blank_page_data])]
        elements.extend(centered_elements)
        elements.append(PageBreak())  # Add a page break after each image

    doc.build(elements)

    # Display the PDF download link
    with open("coloring_book.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    st.download_button(
        label="Download Coloring Book PDF",
        data=pdf_bytes,
        file_name="coloring_book.pdf",
        mime="application/pdf"
    )
