import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the give content to the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file to write, from the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    target_path = os.path.abspath(full_path)
    abs_path = os.path.abspath(working_directory)
    if os.path.commonpath([abs_path,target_path]) != abs_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    parent_directory = os.path.dirname(target_path)
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory, exist_ok=True)

    try:
        with open(target_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
