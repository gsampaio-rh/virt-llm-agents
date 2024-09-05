from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict, Any


class AgentGraphState(TypedDict):
    input: str
    response: Annotated[list, add_messages]


