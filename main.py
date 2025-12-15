import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv



def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if prompt_tokens is None or response_tokens is None:
        raise RuntimeError("Failed API Request")

    if verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print(f"Response:\n {response.text}")

def main():
    print("Hello from ai-agent!")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key = api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    generate_content(client, messages, args.verbose)



    





if __name__ == "__main__":
    main()
