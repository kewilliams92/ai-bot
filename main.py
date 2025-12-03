import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MAX_ITERS = 20

def main():
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ],
    )
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    all_function_responses = []
    iters = 0

    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            break

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            if not response.usage_metadata:
                raise RuntimeError("Gemini API response appears to be malformed")

            if args.verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.candidates:
                for candidate in response.candidates:
                    if candidate.content:
                        for content in candidate.content:
                            if isinstance(content, types.Content):
                                messages.append(content)

            if not response.function_calls:
                # No more function calls, LLM finished
                if response.text.strip():
                    print("Final response:")
                    print(response.text)
                break

            # Execute all function calls
            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=args.verbose)
                if (
                    not function_call_result.parts
                    or not hasattr(function_call_result.parts[0], "function_response")
                    or not hasattr(function_call_result.parts[0].function_response, "response")
                ):
                    raise RuntimeError("Function call did not return a valid response object")

                function_responses.append(function_call_result.parts[0])
                all_function_responses.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            # Append structured function results so LLM can reason
            messages.append(
                types.Content(role="user", parts=function_responses)
            )

        except Exception as e:
            print(f"Error in agent iteration: {e}")
            break

    return 0

if __name__ == "__main__":
    sys.exit(main())

# import os
# import sys
# import argparse
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types
# from functions.get_files_info import schema_get_files_info
# from functions.get_file_content import schema_get_file_content
# from functions.write_file import schema_write_file
# from functions.run_python_file import schema_run_python_file
# from functions.call_function import call_function
# from prompts import system_prompt
#
# load_dotenv()
#
# api_key = os.environ.get("GEMINI_API_KEY")
# client = genai.Client(api_key=api_key)
#
# def main():
#     available_functions = types.Tool(
#         function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
#     )
#     parser = argparse.ArgumentParser(description="Chatbot")
#     parser.add_argument("user_prompt", type=str, help="User prompt")
#     parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
#     args = parser.parse_args()
#     messages = [
#         types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
#     ]
#     response = client.models.generate_content(model="gemini-2.5-flash",contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
#
#     if response.candidates:
#         for candidate in response.candidates:
#             if candidate.content:
#                 for content in candidate.content:
#                     if isinstance(content, types.Content):
#                         messages.append(content)
#
#     if not response.usage_metadata:
#         raise RuntimeError("Gemini API response appears to be malformed")
#     if args.verbose:
#         print(f"User prompt: {args.user_prompt}")
#         print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
#         print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
#     function_calls = response.function_calls
#
#
#     all_function_responses = []
#
#     for _ in range(20):
#         try:
#             response = client.models.generate_content(
#                 model="gemini-2.5-flash",
#                 contents=messages,
#                 config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
#             )
#
#             if response.candidates:
#                 for candidate in response.candidates:
#                     if candidate.content:
#                         for content in candidate.content:
#                             if isinstance(content, types.Content):
#                                 messages.append(content)
#
#             if not response.usage_metadata:
#                 raise RuntimeError("Gemini API response appears to be malformed")
#             if args.verbose:
#                 print(f"User prompt: {args.user_prompt}")
#                 print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
#                 print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
#
#             function_calls = response.function_calls
#
#             if function_calls is not None:
#                 for function_call_part in function_calls:
#                     function_call_result = call_function(function_call_part, verbose=args.verbose)
#                     if not hasattr(function_call_result.parts[0], "function_response") or not hasattr(function_call_result.parts[0].function_response, "response"):
#                         raise RuntimeError("Function call did not return a vaild response object")
#                     all_function_responses.append(function_call_result.parts[0])
#                     if args.verbose:
#                         print(f"-> {function_call_result.parts[0].function_response.response}")
#                     messages.append(
#                         types.Content(
#                             role="user",
#                             parts=[types.Part(text=str(function_call_result.parts[0].function_response.response))]
#                         )
#                     )
#             else:
#                 print("Final response:") 
#                 print(f"{response.text}")
#                 break
#
#         except Exception as e:
#             print(f"Error in agent iteration: {e}")
#             break
#     return 0
#
# if __name__ == "__main__":
#     sys.exit(main())
