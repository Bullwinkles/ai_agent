import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from call_function import available_functions

def main():
    load_dotenv()
    verbose_flag = "--verbose" in sys.argv

    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
            
    if len(args) < 1:
        print("AI coding assistant")
        print('\nUsage: python main.py "Your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
        
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)
    contents = " ".join(args) 
    
    if verbose_flag:
        print(f'\nUser prompt: {contents}')

    messages = [
            types.Content(role = "user", parts = [types.Part(text = contents)]),
    ]

    generate_content(client, messages, verbose_flag)

def generate_content(client, messages, verbose_flag):
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages, 
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt,
            )
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose_flag == True:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        
    if not response.function_calls:
        print("\n" + response.text)
        return response.text
    
    for function in response.function_calls:
        print(f'\nCalling function: {function.name}({function.args})\n')

if __name__ == "__main__":
    main()
