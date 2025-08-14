import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Runs a python file, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The file to run, relative to the working directory.",
                ),
            "args": types.Schema(
                type = types.Type.ARRAY,
                items = types.Schema(
                    type = types.Type.STRING,
                    description = "Optional arguments to pass to the Python file.",
                ),
                description = "Optional arguments to pass to the Python file.",
            ),
        },
        required = ["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'

    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'

    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a python file.'

    commands = ["python", target_path]

    if args:
        commands.extend(args)

    try:
        completed_process = subprocess.run(commands, timeout=30, capture_output=True, text=True, cwd=abs_working_directory)
        output = []

        if completed_process.stdout:
            output.append(f'STDOUT:\n{completed_process.stdout}')
        
        if completed_process.stderr:
            output.append(f'STDERR:\n{completed_process.stderr}')

        if completed_process.returncode !=0:
            output.append(f'Process exited with code {completed_process.returncode}')

        if output:
            return "\n".join(output)
        
        else:
            return f'No output produced.'

    except Exception as e:
        return f'Error: executing python file: {e}.'
