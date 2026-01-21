import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    # 1. Parse CLI arguments
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    # 2. Load API key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Create a .env file with GEMINI_API_KEY='your_key'"
            "and make sure you're running from the project directory."
        )

    client = genai.Client(api_key=api_key)

    # 3. Build structured messages AFTER args exists
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    # 4. Agent loop (limit iterations)
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )

        if response.usage_metadata is None:
            raise RuntimeError("API request failed: no usage metadata returned")

        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # 5. Add model candidates to conversation history
        if not response.candidates:
            raise RuntimeError("API request failed: no candidates returned")

        for candidate in response.candidates:
            if candidate.content is not None:
                messages.append(candidate.content)

        # 6. If no tool calls, we have a final response
        if not response.function_calls:
            print("Final response:")
            print(response.text)
            return

        # 7. Run tool calls and collect tool response parts
        function_results = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            if not function_call_result.parts:
                raise RuntimeError("Function call returned no parts")

            part = function_call_result.parts[0]

            if part.function_response is None:
                raise RuntimeError("Missing function_response")

            if part.function_response.response is None:
                raise RuntimeError("Missing response data")

            function_results.append(part)

            if args.verbose:
                print(f"-> {part.function_response.response}")

        # 8. Add tool results back into conversation history
        messages.append(types.Content(role="user", parts=function_results))

    # 9. If we get here, we hit the iteration cap
    print("Error: reached maximum iterations without a final response.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
