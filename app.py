import streamlit as st
import replicate
import os
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, PageBreak
from reportlab.lib.units import inch

# Set Replicate API token from Streamlit secrets
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.title("Coloring Book PDF Generator")

prompts = st.text_area("Enter your prompts (one per line):")

def add_blank_page(elements):
    elements.append(PageBreak())
    return elements

if st.button("Generate Coloring Book PDF"):
    # Split prompts into a list
    prompt_list = [prompt.strip() for prompt in prompts.split("\n") if prompt.strip()]

    # Run Replicate model on each prompt
    images = []
    for prompt in prompt_list:
        input = {
            "prompt": prompt,
            "negative_prompt": "complex, realistic, color, gradient, cropped, cut off, out of frame",
            "width": 1024,
            "height": 1024
        }
        output = replicate.run(
            "pnickolas1/sdxl-coloringbook:d2b110483fdce03119b21786d823f10bb3f5a7c49a7429da784c5017df096d33",
            input=input
        )
        image_url = output[0]
        images.append(image_url)

    # Create a PDF file with the generated images
    doc = SimpleDocTemplate("coloring_book.pdf", pagesize=(8.5*inch, 11*inch))
    elements = []
    for i, image_url in enumerate(images, start=1):
        if i % 2 != 0:
            response = requests.get(image_url)
            image_file = BytesIO(response.content)
            image = Image(image_file, 8*inch, 8*inch)
            elements.append(image)
        else:
            elements = add_blank_page(elements)

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
