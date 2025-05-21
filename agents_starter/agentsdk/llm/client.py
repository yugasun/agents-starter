from agents import AsyncOpenAI, OpenAIChatCompletionsModel


from ...common.settings import openai_config

# Define a model client. You can use other model client that implements
# the `ChatCompletionClient` interface.
model_client = OpenAIChatCompletionsModel(
    model=openai_config.model,
    openai_client=AsyncOpenAI(
        api_key=openai_config.api_key,
        base_url=openai_config.base_url,
    ),
)
