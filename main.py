import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function
import functions.declarations as func_decs



def main(argv):
    if(len(argv)== 1):
        print("No prompt provided!")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt_args = [arg for arg in argv[1:] if arg != "--verbose"]



    available_functions = types.Tool(
    function_declarations=[
            func_decs.schema_get_file_content,
            func_decs.schema_get_files_info,
            func_decs.schema_run_python_file,
            func_decs.schema_write_file
        ]
    )

    user_prompt = " ".join(prompt_args)
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

-- List files and directories with get_files_info (provide a directory path, use "." for current directory)
- Read file contents with get_file_content (provide the file path)
- Execute Python files with run_python_file (provide the file path and optional arguments)
- Write or overwrite files with write_file (provide file path and content)

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

When listing files, start with the current directory by calling get_files_info with directory="."
"""

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(20):

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]
            ),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)


        if not response.function_calls:
            print(response.text)
            break
        else:
            function_call_result = call_function(response.function_calls[0], ("--verbose" in argv))
            messages.append(function_call_result)

            # Only print if verbose
            if "--verbose" in argv:
                try:
                    response_data = function_call_result.parts[0].function_response.response
                    print(f"-> {response_data}")
                except (AttributeError, IndexError):
                    raise Exception("Function call result missing expected response structure")

    if response.function_calls:
        print(response.text)

    if("--verbose" in argv):

            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main(sys.argv)
