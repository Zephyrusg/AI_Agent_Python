import os
def get_files_info(working_directory, directory=None):
    abs_allowed_root = os.path.abspath(working_directory)
    abs_requested_path = os.path.abspath(os.path.join(working_directory, directory)) 
    project_dir = os.getcwd()
    full_path = os.path.join(working_directory, directory)
    abs_working_directory = os.path.join(project_dir,working_directory)
    abs_full_path = os.path.join(abs_working_directory, directory)
    output_lines = []


    if not abs_requested_path.startswith(abs_allowed_root):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if os.path.isfile(abs_requested_path):
        return (f'Error: "{directory}" is not a directory')
    #output_lines.append(f"abs_requested_path: {abs_requested_path}")
    content = os.listdir(abs_requested_path)
    #output_lines.append(f"content: {content}")
    if directory == ".":
        directory = "current"
    output_lines.append(f"Result for {directory} directory:")
    
    for item in content:
        abs_path_item = os.path.join(abs_requested_path, item)
        output_lines.append(f"- {item}: filesize={os.path.getsize(abs_path_item)} bytes, is_dir={os.path.isdir(abs_path_item)}")

    return "\n".join(output_lines)