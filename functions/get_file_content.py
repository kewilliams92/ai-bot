import os

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    target_path = os.path.abspath(full_path)
    abs_path = os.path.abspath(working_directory)
    if os.path.commonpath([abs_path,target_path]) != abs_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
