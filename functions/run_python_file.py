import os
import subprocess

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