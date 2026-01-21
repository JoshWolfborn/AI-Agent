import os
from google.genai import types

def write_file(working_directory, file_path, content):

    try:  
        
        # Absolute path of the allowed sandbox root
        working_directory_absolute_path = os.path.abspath(working_directory)

        # Build an absolute, normalized target path (prevents ../ escaping tricks)
        file_path_full = os.path.join(working_directory_absolute_path, file_path)
        target_file_path = os.path.normpath(file_path_full)

        # security check
        if os.path.commonpath([working_directory_absolute_path, target_file_path]) != working_directory_absolute_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # correctness check
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # ensure parent directories exist
        parent_directory_path = os.path.dirname(target_file_path)

        if parent_directory_path != "":
            os.makedirs(parent_directory_path, exist_ok=True)

        # write file
        target_file_path_file_object = open(target_file_path, "w")
        try:
            target_file_path_file_object.write(content)
        finally:
            target_file_path_file_object.close()

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as error:
        return f"Error: {error}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes text content to a file relative to the working directory, creating parent directories if needed "
        "and overwriting the file if it already exists. Returns a success message including the number of "
        "characters written, or an error string if the path is invalid or writing fails."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The complete text content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


