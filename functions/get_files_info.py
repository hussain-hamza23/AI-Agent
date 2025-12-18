import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)



def get_files_info(working_directory, directory = "."):
    print(f"Result for {directory} directory...")
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_path, directory))
        valid_path = os.path.commonpath([working_dir_path, target_dir]) == working_dir_path
        
        if not os.path.isdir(target_dir):
            return(f'Error: "{directory}" is not a directory')
        dir_information = []
        if valid_path:
            for dir in os.listdir(path = target_dir):
                full_path = os.path.join(target_dir, dir)
                dir_information.append((f"- {dir}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"))
            return "\n".join(dir_information)
        else:
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    except Exception as e:
        return(f"Error: {e}")


