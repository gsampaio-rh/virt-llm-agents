from datetime import datetime, timezone
import json
import ast


def get_current_utc_datetime():
    now_utc = datetime.now(timezone.utc)
    return now_utc.strftime("%Y-%m-%d %H:%M:%S.%f UTC")[:-3]


def save_json_to_file(json_content, filename=""):
    try:
        # Save the content of json_plan to a file with pretty printing
        with open(filename, "w") as file:
            json.dump(json_content, file, indent=4)  # Indent ensures pretty-printing
        print(f"JSON saved successfully to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


def remove_prefix(input_string: str) -> str:
    prefix = "I have the answer: "
    if input_string.startswith(prefix):
        return input_string[len(prefix) :]
    return input_string


def extract_list_from_string(input_string):
    try:
        # Find the position of the colon and slice the string after it
        list_start = input_string.index("[")
        list_part = input_string[list_start:]

        # Use ast.literal_eval to safely evaluate the list part
        extracted_list = ast.literal_eval(list_part)
        return extracted_list
    except (ValueError, SyntaxError):
        return "Error: Invalid input format."
