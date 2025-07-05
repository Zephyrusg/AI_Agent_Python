import os
def write_file(working_directory, file_path, content):
    abs_allowed_root = os.path.abspath(working_directory)
    abs_requested_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_requested_file.startswith(abs_allowed_root):
        return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

    try:
        dir_path = os.path.dirname(abs_requested_file)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(abs_requested_file, "w") as f:
            f.write(content)
        return(f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)")

    except Exception as e:
       return(f"Error: {str(e)}")
