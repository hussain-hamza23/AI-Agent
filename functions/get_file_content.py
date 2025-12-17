import os
from config import character_limit

def get_file_content(working_directory, file_path):
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_path, file_path))
        valid_path = os.path.commonpath([working_dir_path, target_path]) == working_dir_path

        if not valid_path:
            return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        elif not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        with open(target_path, "r") as f:
            file_content_string = f.read(character_limit)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {character_limit} characters]'

        return file_content_string  
       
    except Exception as e:
        return f"Error: {e}"

    



