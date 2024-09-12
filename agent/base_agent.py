import json
from typing import Dict, Any
from langchain_core.messages.ai import AIMessage
from state.agent_graph import AgentGraphState
from prompt.basic_prompt import SYS_PROMPT
from services.model_service import ModelService
from utils.general.helpers import get_current_utc_datetime


class Agent:

    def __init__(self, state: AgentGraphState, role: str, ollama_service: ModelService):
        """
        Initialize the Agent with a state, role, and model configuration.
        """
        self.state = state
        self.role = role
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

    def work(
        self,
        user_request: str,
        sys_prompt: str = SYS_PROMPT,
    ) -> str:
        """
        Execute a simple task based on the user's request.
        """
        # Define a simple system prompt
        formatted_sys_prompt = sys_prompt.format(datetime=get_current_utc_datetime())
        user_prompt = f"""<|start_header_id|>user<|end_header_id|>\n\n{user_request}<|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>"""

        # Invoke the model with the user's request
        response = self.invoke_model(
            sys_prompt=formatted_sys_prompt, user_prompt=user_prompt
        )

        # Return the processed response
        return {
            f"{self.role}_response": AIMessage(content=response),
        }
