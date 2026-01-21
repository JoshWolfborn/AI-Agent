import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        # 1) Resolve and validate sandbox paths
        working_directory_absolute_path = os.path.abspath(working_directory)

        file_path_full = os.path.join(working_directory_absolute_path, file_path)
        absolute_file_path = os.path.normpath(file_path_full)

        is_inside_working_directory = (
            os.path.commonpath([working_directory_absolute_path, absolute_file_path])
            == working_directory_absolute_path
        )

        if not is_inside_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 2) Must exist and be a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # 3) Must end with .py
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # 4) Build command
        command = ["python", absolute_file_path]
        if args is not None:
            command.extend(args)

        # 5) Run subprocess
        completed_process = subprocess.run(
            command,
            cwd=working_directory_absolute_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # 6) Build output string
        output_parts = []

        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        stdout_text = completed_process.stdout
        stderr_text = completed_process.stderr

        if (stdout_text is None or stdout_text == "") and (stderr_text is None or stderr_text == ""):
            output_parts.append("No output produced")
        else:
            if stdout_text:
                output_parts.append(f"STDOUT:\n{stdout_text}")
            if stderr_text:
                output_parts.append(f"STDERR:\n{stderr_text}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a .py file located within the permitted working directory and returns a combined text result. "
        "The returned string may include 'STDOUT:' and/or 'STDERR:' sections, and may include a nonzero exit code message."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='Path to the Python file to execute, relative to the working directory (must end with ".py")',
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line argument tokens to pass to the program",
            ),
        },
        required=["file_path"],
    ),
)



