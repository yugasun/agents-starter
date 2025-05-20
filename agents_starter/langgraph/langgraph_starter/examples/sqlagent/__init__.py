import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

from typing import Literal
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, create_react_agent

from ...utils import display_image

from .agent import get_prebuild_agent, get_custom_agent
from ...llm.client import model_client as llm

db_path = os.path.join(os.path.dirname(__file__), "Chinook.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()


def run():
    # Prebuilt agent
    agent = get_prebuild_agent(
        llm=llm,
        dialect=db.dialect,
        tools=tools,
    )

    # custom agent
    agent = get_custom_agent(
        llm=llm,
        dialect=db.dialect,
        tools=tools,
    )

    display_image(agent)

    # question = "Which sales agent made the most in sales in 2009?"

    # for step in agent.stream(
    #     {"messages": [{"role": "user", "content": question}]},
    #     stream_mode="values",
    # ):
    #     step["messages"][-1].pretty_print()

    def print_stream(stream):
        for s in stream:
            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()

    inputs = {
        "messages": [("user", "Which sales agent made the most in sales in 2009?")]
    }

    config = {"run_name": "sqlagent", "tags": ["agents_starter"]}

    print_stream(agent.stream(inputs, config, stream_mode="values"))
