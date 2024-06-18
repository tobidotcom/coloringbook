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

# Set the target DPI for the generated images
target_dpi = 300

if st.button("Generate Coloring Book PDF"):
    # Split prompts into a list
    prompt_list = [prompt.strip() for prompt in prompts.split("\n") if prompt.strip()]
    
    # Calculate image dimensions based on the PDF page size and target DPI
    page_width, page_height = letter
    image_width = int(page_width * target_dpi)
    image_height = int(page_height * target_dpi)
    
    # Run Replicate model on each prompt
    images = []
    for prompt in prompt_list:
        output = replicate.run(
            "ai-forever/kandinsky-2.2:ad9d7879fbffa2874e1d909d1d37d9bc682889cc65b31f7bb00d2362619f194a",
            input={"prompt": prompt, "width": image_width, "height": image_height}
        )
        image_url = output[0]  # Assuming the model returns a list with a single URL
        images.append(image_url)
    
    # Create a PDF file with the generated images
    doc = SimpleDocTemplate("coloring_book.pdf", pagesize=letter)
    elements = []
    for image_url in images:
        response = requests.get(image_url)
        image_file = BytesIO(response.content)
        image = Image(image_file, 8.5*inch, 11*inch)  # Fit the image to the page size
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

