from autogen_agentchat.agents import AssistantAgent
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

# from autogen_core.tools import FunctionTool
from autogen_agentchat.ui import Console

from ..llm.client import model_client


# Create an MCP workbench which provides a session to the mcp server.
# refer to: https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.mcp.html#autogen_ext.tools.mcp.mcp_server_tools
async def run():
    # Get the fetch tool from mcp-server-fetch.
    fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
    tools = await mcp_server_tools(fetch_mcp_server)
    # Create an agent that can use the fetch tool.
    agent = AssistantAgent(
        name="fetcher",
        model_client=model_client,
        tools=tools,
        reflect_on_tool_use=True,
    )

    # Let the agent fetch the content of a URL and summarize it.
    await Console(
        agent.run_stream(
            task="Summarize the content of https://microsoft.github.io/autogen/stable/index.html"
        )
    )

    # Close the connection to the model client.
    await model_client.close()
