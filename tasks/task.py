# tasks/task.py


class Task:
    def __init__(
        self, task_id: str, description: str, agent_name: str, data: dict = None, status: str = "pending",
    ):
        self.task_id = task_id
        self.description = description
        self.agent_name = agent_name  # Name of the agent responsible for this task
        self.data = data or {}  # Additional data needed for the task
        self.status = status  # Add a status field

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "agent_name": self.agent_name,
            "data": self.data,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            task_id=task_dict["task_id"],
            description=task_dict["description"],
            agent_name=task_dict["agent_name"],
            data=task_dict.get("data", {}),
            status=task_dict.get("status", "pending"),
        )
