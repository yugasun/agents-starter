from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from ..llm.client import model_client


# refer to: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html#creating-a-team
async def run():
    # Create the primary agent.
    primary_agent = AssistantAgent(
        "primary",
        model_client=model_client,
        system_message="You are a helpful AI assistant.",
    )

    # Create the critic agent.
    critic_agent = AssistantAgent(
        "critic",
        model_client=model_client,
        system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
    )

    # Define a termination condition that stops the task if the critic approves.
    text_termination = TextMentionTermination("APPROVE")

    # Create a team with the primary and critic agents.
    team = RoundRobinGroupChat(
        [primary_agent, critic_agent], termination_condition=text_termination
    )

    await Console(team.run_stream(task="Write a short poem about the fall season."))

    # Close the connection to the model client.
    await model_client.close()
