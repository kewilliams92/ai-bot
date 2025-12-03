import os
from subprocess import run,PIPE
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python script located in the working directory with optional arguments. Output and errors are returned as strings.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the Python file to execute, from the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguements to pass to the Python script."
            )
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    target_path = os.path.abspath(full_path)

    abs_path = os.path.abspath(working_directory)

    if os.path.commonpath([abs_path, target_path]) != abs_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = ["python3", target_path, *args]
        completed_process = run(
            command,
            cwd=working_directory,
            stdout=PIPE,
            stderr=PIPE,
            timeout=30
        )

        stdout_text = completed_process.stdout.decode("utf-8").rstrip()
        stderr_text = completed_process.stderr.decode("utf-8").rstrip()

        output_lines = [f"STDOUT: {stdout_text}", f"STDERR: {stderr_text}"]
        
        if completed_process.returncode != 0:
            output_lines.append(f"Process exited with code {completed_process.returncode}")

        if not stdout_text and not stderr_text and completed_process.returncode == 0:
            return "No output produced"

        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"
