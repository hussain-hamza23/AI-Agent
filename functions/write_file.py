import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes provided content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory. If not provided, creates the new file.",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description="The contents to write to the file"
            ),
        },
        required=["file_path","content"],
    ),
)

def write_file(working_directory, file_path, content):
    abs_directory = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abs_directory, file_path))
    valid_path = os.path.commonpath([abs_directory, target_path]) == abs_directory

    if not valid_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: "{file_path}" is a directory'
        
    if not os.path.exists(target_path) and valid_path:
        try:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
        except Exception as e:
            return f'Could not make "{file_path}" directory: {e}'
        

    with open(target_path, "w") as w:
        try:
            w.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Could not write to file: {e}"
