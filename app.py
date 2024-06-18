from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
import streamlit as st  # Import streamlit first

# Initialize OpenAI client with API key from Streamlit secrets

def generate_mandala_prompt(prompt):
    messages = [
        {"role": "system", "content": "You are an AI assistant specializing in generating detailed and compelling prompts for creating coloring book mandala images. Your task is to take a given prompt and enhance it by adding vivid descriptions, imaginative concepts, and specific details that would make for an engaging and visually appealing black and white coloring book page mandala."},
        {"role": "user", "content": f"Generate a detailed and compelling black and white coloring book page mandala prompt based on the following: {prompt}"}
    ]

    response = client.chat.completions.create(model="gpt-4o",
    messages=messages,
    max_tokens=4096,
    n=1,
    stop=None,
    temperature=0.7)

    generated_prompt = response.choices[0].message.content.strip() + " black and white coloring book page mandala"

    return generated_prompt

# Initialize OpenAI client with API key from Streamlit secrets

# Generate 100 coloring book mandala prompts
prompts = []
for i in range(100):
    initial_prompt = "A mandala design inspired by..."  # Replace with your desired initial prompt
    generated_prompt = generate_mandala_prompt(initial_prompt)
    prompts.append(generated_prompt)

# Print the generated prompts
for prompt in prompts:
    print(prompt)
    print()
