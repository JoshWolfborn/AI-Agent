import os
from google.genai import types

# config.py at project root
from config import READ_FILE_MAXIMUM_CHARACTERS

def get_file_content(working_directory, file_path):
        try:

            # Absolute path of the allowed sandbox root
            working_directory_absolute_path = os.path.abspath(working_directory)

            # Build an absolute, normalized target path (prevents ../ escaping tricks)
            file_path_full = os.path.join(working_directory_absolute_path, file_path)
            target_file_path = os.path.normpath(file_path_full)

            # security check
            if os.path.commonpath([working_directory_absolute_path, target_file_path]) != working_directory_absolute_path:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

            # Must be a regular file
            if not os.path.isfile(target_file_path):
                return f'Error: File not found or is not a regular file: "{file_path}"'
            
            with open(target_file_path, "r", encoding="utf-8", errors="replace") as target_file_path_file_object:
                
                content = target_file_path_file_object.read(READ_FILE_MAXIMUM_CHARACTERS)
            
                if target_file_path_file_object.read(1):
                    content += f'[...File "{file_path}" truncated at {READ_FILE_MAXIMUM_CHARACTERS} characters]'
            
            return content
        
        except Exception as e:
            return f"Error: {e}"
        
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the text contents of a file relative to the working directory. Returns an error string if the file is outside the permitted directory, does not exist, or is not a regular file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)


