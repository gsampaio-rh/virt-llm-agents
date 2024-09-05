# Example schema for validating the agent's output
output_schema = {
    "type": "object",
    "properties": {
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",  # Unique identifier for the task.
                    },
                    "task_name": {
                        "type": "string",  # Short name of the task (e.g., "Validate VMware Access").
                    },
                    "task_description": {
                        "type": "string",  # Detailed description of the task to be executed.
                    },
                    "agent": {
                        "type": "string",
                        "enum": [
                            "architect",
                            "ocp_engineer",
                            "vsphere_engineer",
                            "networking",
                            "reviewer",
                            "cleanup",
                        ],  # Agent responsible for executing the task.
                    },
                    "status": {
                        "type": "string",
                        "enum": [
                            "pending",
                            "in_progress",
                            "completed",
                            "failed",
                        ],  # Current status of the task.
                    },
                    "dependencies": {
                        "type": "array",
                        "items": {
                            "type": "string",  # Task IDs that must be completed before this task can start.
                        },
                        "default": [],  # Default is an empty array if there are no dependencies.
                    },
                    "acceptance_criteria": {
                        "type": "string",  # Criteria that must be met to consider the task successfully completed.
                    },
                    "tool_to_use": {
                        "type": [
                            "string",
                            "null",
                        ],  # The tool the agent should use, or null if no tool is required.
                        "default": None,  # Default is None if no tool is specified.
                    },
                    "provided_inputs": {
                        "type": "object",  # Input data needed for this task.
                        "additionalProperties": {
                            "type": ["null", "string", "array"],
                            "items": {"type": "string"},
                        },
                        "default": {},  # Default is an empty object if no inputs are provided.
                    },
                },
                "required": [
                    "task_id",
                    "task_name",
                    "task_description",
                    "agent",
                    "status",
                    "acceptance_criteria",
                ],  # Dependencies, tool_to_use, and provided_inputs are optional.
            },
        }
    },
    "required": ["tasks"],
}
