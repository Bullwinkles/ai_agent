import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():

    verbose_flag = "--verbose" in sys.argv

    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
            
    if len(args) < 1:
        print("Please provide a prompt for the ai.")
        sys.exit(1)
        
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)
    model = "gemini-2.0-flash-001"
    contents = " ".join(args) 
    
    messages = [
            types.Content(role = "user", parts = [types.Part(text = contents)]),
    ]

    response = client.models.generate_content(model = model, contents = messages)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose_flag == True:
        
        print("\n" + response.text)
        print(f"User prompt: {contents}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        
    else:
        
        print("\n" + response.text)
    
if __name__ == "__main__":
    main()
