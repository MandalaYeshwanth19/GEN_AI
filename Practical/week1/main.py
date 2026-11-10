
from dotenv import load_dotenv
from google import genai
import os
import time

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

# Initialize Gemini
client = genai.Client(api_key=api_key)

# Try multiple available models
models = [
    "gemini-3.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.8-flash"
]

prompt = "What is Artificial Intelligence? Explain in simple words."

success = False

for model in models:
    print(f"\nTrying model: {model}")

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            print("\n========== LLM RESPONSE ==========")
            print(response.text)
            print("==================================")

            success = True
            break

        except Exception as e:
            error = str(e)

            if "503" in error or "UNAVAILABLE" in error:
                print("Gemini server busy. Trying again...")
                time.sleep(3)

            elif "429" in error or "RESOURCE_EXHAUSTED" in error:
                print("API quota or rate limit reached.")
                break

            else:
                print("Gemini API Error:", e)
                break

    if success:
        break

if not success:
    print("\nAll models failed. Please try again later.")
