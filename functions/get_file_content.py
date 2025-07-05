import os
def get_file_content(working_directory, file_path):

    abs_allowed_root = os.path.abspath(working_directory)
    abs_requested_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_requested_file.startswith(abs_allowed_root):
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(abs_requested_file):
        return (f'Error: File not found or is not a regular file: "{file_path}"')
    MAX_CHARS = 10000

    try:
        with open(abs_requested_file, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > 10000:
                truncated_content = file_content_string[:MAX_CHARS]
                truncation_message = f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
                return (truncated_content + truncation_message)
            else:
                return (file_content_string)
    except Exception as e:
        return(f"Error: {str(e)}")


