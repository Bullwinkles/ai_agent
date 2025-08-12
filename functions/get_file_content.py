import os
from config import input_limit

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, "r") as f:
            input_text = f.read(input_limit)
            if os.path.getsize(target_file) > input_limit:
                return f'{input_text}[...File "{file_path}" truncated at {input_limit} characters]'

            else:
                return input_text

    except Exception as e:
        return f'Error reading file contents: {e}'
        
