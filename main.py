import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from config import WORKING_DIRECTORY, MAX_ITERATIONS
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_files_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

def call_function(function_call_part, verbose = False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file":write_file,
        "run_python_file":run_python_file
    }
    if function_call_part.name not in functions:
     return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )
      
    arguments = dict(function_call_part.args)
    arguments["working_directory"] = WORKING_DIRECTORY
    chosen_function = functions[function_call_part.name]

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": chosen_function(**arguments)},
            )
        ],
    )


def generate_content(client, messages: list, verbose, available_functions):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    if prompt_tokens is None or response_tokens is None:
        raise RuntimeError("Failed API Request")
    
    if response.candidates and response.candidates is not None:
        for message in response.candidates:
            messages_in_response = message.content
            messages.append(messages_in_response)

    if response.function_calls:
        call_response = []
        for function in response.function_calls:
            result = call_function(function, verbose)
            if not result.parts or not result.parts[0].function_response or result.parts[0].function_response.response is None:
                raise Exception("Error: Empty funcion call result")
            
            call_response.append(result.parts[0])
            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
        messages.append(types.Content(role="user",parts=call_response))
        return response

    return response.text


    

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
    available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_files_content,schema_write_file,schema_run_python_file],)

    count = 0
    while count < MAX_ITERATIONS:
        try:
            response = generate_content(client, messages, args.verbose,available_functions)
            if isinstance(response, str) and response != "":
                print(f"Final Response:\n{response}")
                break  
            count += 1
        except Exception as e:
            print(f"Error: has occured {e}")

if __name__ == "__main__":
    main()
