from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from ..llm.client import model_client


async def run():
    assistant = AssistantAgent("assistant", model_client=model_client)
    user_proxy = UserProxyAgent(
        "user_proxy", input_func=input
    )  # Use input() to get user input from console.

    # Create the termination condition which will end the conversation when the user says "APPROVE".
    termination = TextMentionTermination("APPROVE")

    # Create the team.
    team = RoundRobinGroupChat(
        [assistant, user_proxy], termination_condition=termination
    )

    # Run the conversation and stream to the console.
    stream = team.run_stream(task="Write a 4-line poem about the ocean.")
    # Use asyncio.run(...) when running in a script.
    await Console(stream)

    await model_client.close()
