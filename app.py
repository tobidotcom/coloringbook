import streamlit as st
import replicate
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib.units import inch

# Set Replicate API key from Streamlit secrets
replicate.init(api_key=os.environ.get("REPLICATE_API_KEY"))

st.title("Coloring Book PDF Generator")

prompts = st.text_area("Enter your prompts (one per line):")

if st.button("Generate Coloring Book PDF"):
    # Split prompts into a list
    prompt_list = [prompt.strip() for prompt in prompts.split("\n") if prompt.strip()]
    
    # Run Replicate model on each prompt
    images = []
    for prompt in prompt_list:
        output = replicate.run(
            "ai-forever/kandinsky-2.2:ad9d7879fbffa2874e1d909d1d37d9bc682889cc65b31f7bb00d2362619f194a",
            input={"prompt": prompt}
        )
        images.append(output)
    
    # Create a PDF file with the generated images
    doc = SimpleDocTemplate("coloring_book.pdf", pagesize=letter)
    elements = []
    for image_url in images:
        image = Image(image_url, 6*inch, 6*inch)
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
