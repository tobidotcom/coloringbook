import openai
import streamlit as st

# Set up OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

# Function to generate image prompts
def generate_image_prompts(topic, num_prompts):
    prompt = f"Generate {num_prompts} creative and unique prompts for black and white coloring book page mandalas on the topic of {topic}. Separate each prompt with a line break."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-0125",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    prompts = response.choices[0].text.strip().split("\n")
    return prompts

# Streamlit app
def main():
    st.title("Coloring Book Image Generator")
    topic = st.text_input("Enter a topic for the image prompts")
    num_prompts = st.number_input("Number of prompts to generate", min_value=1, max_value=100, value=10)
    
    if st.button("Generate Prompts"):
        with st.spinner("Generating prompts..."):
            prompts = generate_image_prompts(topic, num_prompts)
        st.success("Prompts generated successfully!")
        st.write("Generated Prompts:")
        for prompt in prompts:
            st.write(f"- {prompt}")

if __name__ == "__main__":
    main()
