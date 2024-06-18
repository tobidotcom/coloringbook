import streamlit as st
import replicate
import os
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib.units import inch

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
            "negative_prompt": "complex, realistic, color, gradient"
        }
        prediction = replicate.predictions.create(
            "cbaf592788a0513ff5ca3beecdc0d9280fb44908771656f2adef630a263d9ebe",
            input=input
        )
        image_url = prediction.output[0]  # Assuming the model returns a list with a single URL
        images.append(image_url)

    # Create a PDF file with the generated images
    doc = SimpleDocTemplate("coloring_book.pdf", pagesize=letter)
    elements = []
    for image_url in images:
        response = requests.get(image_url)
        image_file = BytesIO(response.content)
        image = Image(image_file, 6*inch, 6*inch)
        elements.append(image)
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
