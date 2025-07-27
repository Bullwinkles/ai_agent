import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():

    verbose_flag = False

    if len(sys.argv) < 2:
        print("Please provide a prompt for the ai.")
        sys.exit(1)
        
    if "--verbose" in sys.argv:
        verbose_flag = True
        
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)
    model = "gemini-2.0-flash-001"
    contents = sys.argv[1]
    
    messages = [
            types.Content(role = "user", parts = [types.Part(text = contents)]),
    ]

    response = client.models.generate_content(model = model, contents = messages)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose_flag == True:
        
        print(response.text)
        print(f"User prompt: {contents}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        
    else:
        
        print(response.text)
    
if __name__ == "__main__":
    main()
