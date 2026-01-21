import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    try:

        working_directory_absolute_path = os.path.abspath(working_directory)

        directory_full_path = os.path.join(working_directory_absolute_path, directory)

        target_directory = os.path.normpath(directory_full_path)

        # Will be True or False
        validated_target_directory = os.path.commonpath([working_directory_absolute_path, target_directory]) == working_directory_absolute_path

        # security check
        if not validated_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # correctness check
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        items_info = []

        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)

            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            items_info.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(items_info)
    
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

        
