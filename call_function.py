# call_function.py

from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file


# 1) Tool declaration list the model can call
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)


# 2) Map schema function names -> real Python functions
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call, verbose=False):
    """
    Dispatches a Gemini types.FunctionCall to the correct local Python function and
    returns a types.Content(tool response) containing either a result or an error.
    """
    function_name = function_call.name or ""

    # Print call info
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")

    # Validate function name
    target_function = function_map.get(function_name)
    if target_function is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Copy args (so we can safely overwrite / inject values)
    args = dict(function_call.args) if function_call.args else {}

    # Enforce sandbox root (course convention)
    args["working_directory"] = "calculator"

    # Execute and wrap response
    try:
        result = target_function(**args)

        # If the function itself returned an "Error: ..." string, treat it as an error
        if isinstance(result, str) and result.startswith("Error:"):
            payload = {"error": result}
        else:
            payload = {"result": result}

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response=payload,
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )
