import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a specificed file, constrainted to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file to read, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    target_path = os.path.abspath(full_path)
    abs_path = os.path.abspath(working_directory)
    if os.path.commonpath([abs_path,target_path]) != abs_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_COUNT = 10000

    try:
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_COUNT)
            extra = f.read(1)
            if extra:
                file_content_string += f' [...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
