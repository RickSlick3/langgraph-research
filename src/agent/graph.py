"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

import getpass
import os
from langchain.chat_models import init_chat_model

from langgraph.checkpoint.memory import MemorySaver


import os

from dotenv import load_dotenv

from typing import Annotated, List

from langchain_core.tools import tool
from langchain.chat_models import init_chat_model

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import MemorySaver

from pydantic import BaseModel, Field


api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key
model = init_chat_model("openai:gpt-4.1")


class Context(TypedDict):
    """Context parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    my_configurable_param: Annotated[list, add_messages]


@dataclass
class State:
    """Input state for the agent.

    Defines the initial structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    """

    user_input: str = "example"

# class State(TypedDict):
#     # Messages have the type "list". The `add_messages` function
#     # in the annotation defines how this state key should be updated
#     # (in this case, it appends messages to the list, rather than overwriting them)
#     messages: Annotated[list, add_messages]


async def call_model(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Process input and returns output.

    Can use runtime context to alter behavior.
    """
    user_message = state.user_input
    response = model.invoke(user_message)
    return {"user_input": response.content}
    # return {
    #     "changeme": response.content
    #     # f"Configured with {runtime.context.get('my_configurable_param')}"
    # }

# memory = MemorySaver()
# app = workflow.compile(checkpointer=memory)

# Define the graph
graph = (
    StateGraph(State, context_schema=Context)
    .add_node(call_model)
    .add_edge("__start__", "call_model")
    .compile(name="New Graph")
)
