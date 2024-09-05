from jsonschema import validate, ValidationError
import json

def validate_agent_output(json_content: dict, schema: dict):
    """
    Validate the agent's output against the provided schema.
    """
    try:
        validate(instance=json_content, schema=schema)
        feedback_message = (
            """<|start_header_id|>assistant<|end_header_id|>\n\nLGTM<|eot_id|>"""
        )
        return True, feedback_message
    except ValidationError as e:
        feedback_message = (
            f"""<|start_header_id|>assistant<|end_header_id|>\n\{e.message}<|eot_id|>"""
        )
        return False, feedback_message
