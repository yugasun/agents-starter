from autogen_ext.models.openai import OpenAIChatCompletionClient

from ..settings import openai_config


# Define a model client. You can use other model client that implements
# the `ChatCompletionClient` interface.
model_client = OpenAIChatCompletionClient(
    model=openai_config.model,
    api_key=openai_config.api_key,
    base_url=openai_config.base_url,
    # should convert the model info model to a model info object
    model_info=openai_config.model_info.model_dump(),
)
