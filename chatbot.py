import os
from dotenv import load_dotenv
import chainlit as cl
import google.generativeai as genai

# Load .env
load_dotenv()

# Load API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-lite")


@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip().lower()

    # Study Buddy prompt selector
    if "quiz" in user_input:
        prompt = f"Create a short quiz with 30 questions on the topic: {user_input}"
    elif "tip" in user_input or "advice" in user_input:
        prompt = f"Give useful study tips for students related to: {user_input}"
    elif "motivation" in user_input or "quote" in user_input:
        prompt = "Share an inspiring motivational quote for students who are studying hard."
    elif "exam" in user_input or "prepare" in user_input:
        prompt = f"Explain how to prepare effectively for exams related to: {user_input}"
    elif "note" in user_input or "summary" in user_input:
        prompt = f"Provide a concise summary or notes on the topic: {user_input}"
    else:
        prompt = f"Answer this study-related question creatively and clearly: {user_input}"

    try:
        response = model.generate_content(prompt)
        await cl.Message(content=response.text).send()
    except Exception as e:
        await cl.Message(content=f"❗ Error: {str(e)}").send()
