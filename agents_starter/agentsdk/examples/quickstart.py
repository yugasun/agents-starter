from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner

from pydantic import BaseModel

from ..agent import AgentSDK


class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str


async def run():
    guardrail_agent = AgentSDK(
        name="Guardrail check",
        instructions="""Check if the user is asking about homework, output json format '{"is_homework": bool, "reasoning": "explain why"}' if it is homework, otherwise output json format '{"is_homework": false, "reasoning": ""}'""",
        output_type=HomeworkOutput,
    )

    math_tutor_agent = AgentSDK(
        name="Math Tutor",
        handoff_description="Specialist agent for math questions",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    )

    history_tutor_agent = AgentSDK(
        name="History Tutor",
        handoff_description="Specialist agent for historical questions",
        instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    )

    async def homework_guardrail(ctx, agent, input_data):
        print(f"Guardrail check input: {input_data}")
        result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
        final_output = result.final_output_as(HomeworkOutput)
        print(f"Guardrail check result: {final_output}")
        print(f"Guardrail check reasoning: {final_output.reasoning}")
        print(f"Guardrail check is homework: {final_output.is_homework}")
        return GuardrailFunctionOutput(
            output_info=final_output,
            tripwire_triggered=not final_output.is_homework,
        )

    triage_agent = AgentSDK(
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's homework question",
        handoffs=[history_tutor_agent, math_tutor_agent],
        input_guardrails=[
            InputGuardrail(guardrail_function=homework_guardrail),
        ],
    )

    # result = await Runner.run(
    #     triage_agent, "who was the first president of the united states?"
    # )
    # print(result.final_output)

    result = await Runner.run(triage_agent, "what is life")
    print(result.final_output)
