from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console

# from autogen_core.tools import FunctionTool

from ..llm.client import model_client


# Define a tool using a Python function.
async def web_search(query: str) -> str:
    """Find information on the web"""
    return "AutoGen is a programming framework for building multi-agent applications."


# Create an MCP workbench which provides a session to the mcp server.
# refer to: https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.mcp.html#autogen_ext.tools.mcp.mcp_server_tools
async def run():
    # Create an agent that can use the fetch tool.
    agent = AssistantAgent(
        name="fetcher",
        model_client=model_client,
        tools=[web_search],
        reflect_on_tool_use=True,
        system_message="Use tools to solve tasks.",
    )

    # Let the agent fetch the content of a URL and summarize it.
    await Console(agent.run_stream(task="Find information on AutoGen"))

    # Close the connection to the model client.
    await model_client.close()
