import requests
import json
from typing import Dict, Any, Optional


class ModelService:
    def __init__(
        self,
        model: str,
        temperature: float = 0.0,
        top_p: float = 1.0,
        top_k: int = 0,
        repetition_penalty: float = 1.0,
        stop: Optional[list] = None,
        model_endpoint: str = "http://localhost:11434/api/generate",
    ):
        self.config = {
            "model_endpoint": model_endpoint,
            "model": model,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "repetition_penalty": repetition_penalty,
            "headers": {"Content-Type": "application/json"},
            "stop": stop,
        }

    def prepare_payload(
        self, user_prompt: str, sys_prompt: str, stream: bool = False
    ) -> Dict[str, Any]:
        return {
            "model": self.config.get("model"),
            "format": "json",
            "prompt": user_prompt,
            "system": sys_prompt,
            "stream": stream,
            "temperature": self.config.get("temperature"),
            "top_p": self.config.get("top_p"),
            "top_k": self.config.get("top_k"),
            "repetition_penalty": self.config.get("repetition_penalty"),
            "stop": self.config.get("stop"),
        }

    def request_model_generate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                self.config["model_endpoint"],
                headers=self.config.get("headers"),
                data=json.dumps(payload),
                timeout=30,
            )
            response.raise_for_status()

            if response.content.strip():
                return response.json()
            else:
                return {"error": "Empty response from model"}
        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def process_model_response(self, response_json: Dict[str, Any]) -> str:
        try:
            # Handle the response data and format it as needed
            response_content = json.loads(response_json.get("response", "{}"))
            pretty_content = json.dumps(response_content, indent=4)
            return pretty_content
        except json.JSONDecodeError:
            return "Error processing the response"

