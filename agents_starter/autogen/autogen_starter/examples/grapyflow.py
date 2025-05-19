from autogen_agentchat.agents import (
    AssistantAgent,
    MessageFilterAgent,
    MessageFilterConfig,
    PerSourceFilter,
)
from autogen_agentchat.teams import (
    DiGraphBuilder,
    GraphFlow,
)
from autogen_agentchat.ui import Console
from ..llm.client import model_client


async def run():
    # Agents
    generator = AssistantAgent(
        "generator",
        model_client=model_client,
        system_message="Generate a list of creative ideas.",
    )
    reviewer = AssistantAgent(
        "reviewer",
        model_client=model_client,
        system_message="Review ideas and say 'REVISE' and provide feedbacks, or 'APPROVE' for final approval.",
    )
    summarizer_core = AssistantAgent(
        "summary",
        model_client=model_client,
        system_message="Summarize the user request and the final feedback.",
    )

    # Filtered summarizer
    filtered_summarizer = MessageFilterAgent(
        name="summary",
        wrapped_agent=summarizer_core,
        filter=MessageFilterConfig(
            per_source=[
                PerSourceFilter(source="user", position="first", count=1),
                PerSourceFilter(source="reviewer", position="last", count=1),
            ]
        ),
    )

    # Build graph with conditional loop
    builder = DiGraphBuilder()
    builder.add_node(generator).add_node(reviewer).add_node(filtered_summarizer)
    builder.add_edge(generator, reviewer)
    builder.add_edge(reviewer, generator, condition="REVISE")
    builder.add_edge(reviewer, filtered_summarizer, condition="APPROVE")
    builder.set_entry_point(
        generator
    )  # Set entry point to generator. Required if there are no source nodes.
    graph = builder.build()

    # Create the flow
    flow = GraphFlow(
        participants=builder.get_participants(),
        graph=graph,
    )

    # Run the flow and pretty print the output in the console
    await Console(flow.run_stream(task="Brainstorm ways to reduce plastic waste."))

    model_client.close()
