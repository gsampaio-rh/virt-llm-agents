from langchain.tools.render import render_text_description_and_args


def get_tools_name(tools_list):
    """Receives a list of tool objects and returns a list of their names."""
    return [tool.name for tool in tools_list]

def get_tools_description(tools_list):
    return (
        render_text_description_and_args(tools_list)
        .replace("{", "{{")
        .replace("}", "}}")
    )

