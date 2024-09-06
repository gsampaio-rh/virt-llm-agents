import json
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import SystemMessage
from termcolor import colored
from state.agent_graph import AgentGraphState
from services.model_service import ModelService
from prompt.react_prompt import DEFAULT_SYS_REACT_PROMPT
from utils.general.helpers import get_current_utc_datetime
from utils.general.tools import get_tools_name, get_tools_description

class ReactAgent:

    def __init__(self, state: AgentGraphState, role: str, tools: list, ollama_service: ModelService):
        """
        Initialize the Agent with a state, role, and model configuration.
        """
        self.state = state
        self.role = role
        self.tools = tools
        self.ollama_service = ollama_service

    def invoke_model(self, sys_prompt: str, user_prompt: str):
        """
        Prepare the payload, send the request to the model, and process the response.
        """
        # Prepare the payload
        payload = self.ollama_service.prepare_payload(
            user_prompt,
            sys_prompt,
        )

        # Invoke the model and get the response
        response_json = self.ollama_service.request_model_generate(
            payload,
        )

        # Process the model's response
        response_content = self.ollama_service.process_model_response(response_json)

        # Return the processed response
        return response_content

    def write_react_prompt(
        self,
        user_prompt: str = "",
        agent_scratchpad: str = "",
    ) -> str:
        return DEFAULT_SYS_REACT_PROMPT.format(
            user_prompt=user_prompt,
            agent_scratchpad=agent_scratchpad,
            tools_name=get_tools_name(self.tools),
            tools_description=get_tools_description(self.tools),
            datetime=get_current_utc_datetime(),
        )

    # Function to format the scratchpad into a properly indented string
    def format_scratchpad(self, scratchpad):
        formatted_output = ""
        for entry in scratchpad:
            formatted_output += entry.strip() + "\n"
        return formatted_output

    def react(self, user_request: str) -> dict:
        """
        Execute the task based on the user's request by following the thought → action → observation loop.
        """

        answer = None

        # Start with the user's request as the first input
        user_prompt = (
            f"""<|start_header_id|>user<|end_header_id|>\n\n{user_request}<|eot_id|>"""
        )

        sys_prompt = self.write_react_prompt(user_prompt=user_prompt)
        # user_prompt = user_request
        tool_response = None
        action = None
        action_input = None
        scratchpad = []

        print(colored(user_prompt, "green"))

        # Loop until a final answer is generated
        while answer is None:
            # Invoke the model with the system prompt and current user input

            response = self.invoke_model(sys_prompt=sys_prompt, user_prompt=user_prompt)

            try:
                # Parse the response assuming it's in JSON format
                response_dict = json.loads(
                    response
                )  # Assuming response is a JSON object

                assistant_message = f"""<|start_header_id|>assistant<|end_header_id|>\n\n{response}<|eot_id|>"""

                print(colored(assistant_message, "cyan"))

                scratchpad.append(assistant_message)

                formatted_scratchpad = self.format_scratchpad(scratchpad)
                sys_prompt = self.write_react_prompt(
                    user_prompt=user_prompt, agent_scratchpad=formatted_scratchpad
                )

                action = response_dict.get("action", None)
                action_input = response_dict.get("action_input", None)

                # If there is an action, execute the corresponding tool
                if action:
                    status, tool_response = self.execute_tool(action, action_input)

                    # Formulate the observation to feed back into the model
                    tool_response_dict = {
                        "observation": tool_response,
                    }

                    tool_response_json = json.dumps(tool_response_dict, indent=4)

                    result_message = f"""<|start_header_id|>ipython<|end_header_id|>\n\n{tool_response_json}<|eot_id|>"""

                    print(colored(result_message, "yellow"))

                    user_prompt = tool_response_json

                # Check if the model has given an answer
                if "answer" in response_dict:
                    answer = response_dict["answer"]

            except Exception as e:
                print(str(e))
                system_message = f"""<|start_header_id|>ipython<|end_header_id|>\n\n{str(e)}<|eot_id|>"""
                scratchpad.append(system_message)
                formatted_scratchpad = self.format_scratchpad(scratchpad)
                sys_prompt = self.write_react_prompt(
                    user_prompt=user_prompt, agent_scratchpad=formatted_scratchpad
                )

        # Return the final answer
        return {
            "response": AIMessage(content=answer),
            "tool_response": SystemMessage(content=str(tool_response)),
        }

    def execute_tool(self, action: str, action_input: dict):
        """
        Simulate the tool execution based on the action and action_input.
        In a real-world scenario, this would call the appropriate tool.
        """
        # Simulate some tool actions (this would be replaced by actual tool logic)
        tool_message = f"""<|python_tag|>{action}.call({action_input})\n<|eom_id|>"""
        print(
            colored(
                tool_message,
                "magenta",
            )
        )

        for tool in self.tools:
            if tool.name == action:
                try:
                    result = tool.invoke(action_input)
                    result_message = f"""<|start_header_id|>ipython<|end_header_id|>\n\n{result}<|eot_id|>"""
                    print(colored(result_message, "magenta"))
                    return True, result
                except Exception as e:
                    return False, f"Error executing tool {action}: {str(e)}"
        else:
            return f"Tool {action} not found or unsupported operation."
