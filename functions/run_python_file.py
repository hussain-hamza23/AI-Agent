import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abs_path,file_path))
    valid_path = os.path.commonpath([abs_path,target_path]) == abs_path

    if not valid_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(target_path):
        return f'Error: File "{file_path}" does not exist.'
    
    try:
        if file_path.endswith(".py"):
            cmd = ["python", file_path]
            if args:
                cmd.extend(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=abs_path,
                timeout=30
            )

            if result.returncode == 0:
                return f'- STDOUT: {result.stdout}\n - STDERR: {result.stderr}\n -Process exited with code {result.returncode}'
            else:
                return "No output produced"
        else:
            return f'Error: "{file_path}" is not a Python file'
    except Exception as e:
        return f'Error: executing Python file: {e}'