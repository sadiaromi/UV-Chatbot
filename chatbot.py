import os
from dotenv import load_dotenv
import chainlit as cl

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

# Load .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❗ GEMINI_API_KEY not found in .env")

# Setup Gemini using OpenAI-compatible format
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Create Agent
agent = Agent(
    name="StudyBuddy",
    model=model
)

runner = Runner()

@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content.strip().lower()

    if "quiz" in user_input:
        prompt = f"Create a quiz with 30 questions on the topic: {user_input}"
    elif "tip" in user_input or "advice" in user_input:
        prompt = f"Give useful study tips for: {user_input}"
    elif "motivation" in user_input or "quote" in user_input:
        prompt = "Share a motivational quote for students."
    elif "exam" in user_input or "prepare" in user_input:
        prompt = f"How to prepare for exams on: {user_input}"
    elif "note" in user_input or "summary" in user_input:
        prompt = f"Provide a summary of: {user_input}"
    else:
        prompt = f"Answer this student question: {user_input}"

    try:
        # Run agent
        result = await runner.run(
            input=prompt,
            starting_agent=agent
        )

       
        output = result.final_output  # ✅ This shows just the model's response

        await cl.Message(content=output).send()

    except Exception as e:
        await cl.Message(content=f"❗ Error: {str(e)}").send()
