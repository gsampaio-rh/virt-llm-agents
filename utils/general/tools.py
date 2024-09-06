from langchain.tools.render import render_text_description_and_args
from typing import Dict, Any
from langchain_core.tools import BaseTool
import json


def get_tools_name(tools_list):
    """Receives a list of tool objects and returns a list of their names."""
    return [tool.name for tool in tools_list]

def get_tools_description(tools_list):
    return (
        render_text_description_and_args(tools_list)
        .replace("{", "{{")
        .replace("}", "}}")
    )


def get_tool_description_json(tool: BaseTool) -> Dict[str, Any]:
    # Get the tool's name
    tool_name = tool.name

    # Get the tool's description
    description = tool.description

    # Retrieve the argument schema
    params = {}
    if tool.args_schema:
        for field_name, field_info in tool.args_schema.__fields__.items():
            param_type = (
                field_info.type_.__name__
                if not hasattr(field_info.type_, "__origin__")
                else str(field_info.type_).replace("typing.", "")
            )
            param_info = {
                "param_type": param_type,
                "description": field_info.field_info.description
                or "No description available",
                "required": field_info.required,
            }
            params[field_name] = param_info

    # Format the final dictionary
    tool_json = {"name": tool_name, "description": description, "parameters": params}

    return tool_json

def get_tools_description_json(tools_list):
    tools_json = []

    for tool in tools_list:
        tool_json = get_tool_description_json(tool)
        tools_json.append(tool_json)

    return tools_json
