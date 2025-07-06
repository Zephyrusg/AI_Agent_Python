import os
import subprocess

def run_python_file(working_directory, file_path):


    abs_allowed_root = os.path.abspath(working_directory)
    abs_requested_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_requested_file.startswith(abs_allowed_root):
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.exists(abs_requested_file):
        return (f'Error: File "{file_path}" not found.')
    if not abs_requested_file.endswith(".py"):
        return (f'Error: "{file_path}" is not a Python file.')
    output_lines = []
    try:
        result = subprocess.run(["python3",  f"{abs_requested_file}"],timeout=30, capture_output=True, text=True )
    except Exception as e:
        return(f"Error: executing Python file: {e}")

    if result.stdout:
        output_lines.append(f"STDOUT: {result.stdout}")
    if result.stderr:
        output_lines.append(f"STDERR: {result.stderr}")
    if result.returncode != 0:
        output_lines.append(f"Process exited with code {result.returncode}")
    if len(output_lines) == 0:
        return "No output produced."
    else:
        return("\n".join(output_lines))
