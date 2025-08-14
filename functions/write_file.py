import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Creates and writes the contents of the specified file, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The file to write the contents to. If it does not exist it will be created." 
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "The content to write to file.",
            ),
        },
        required = ["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside of the working directory.'

    if not os.path.exists(target_file):
        try:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
        except Exception as e:
            return f'Error: creating directory: {e}.'

    if os.path.exists(target_file) and os.path.isdir(target_file):
        return f'Error: {file_path} is a directory, not a file.'
    
    try:
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written).'

    except Exception as e:
        return f'Error: Failed to write to file: {e}.'
