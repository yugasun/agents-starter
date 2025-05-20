import litellm
from crewai import LLM

from ..settings import openai_config

litellm.api_key = openai_config.api_key
litellm.api_base = openai_config.base_url

# Define a model client. You can use other model client that implements
# the `ChatCompletionClient` interface.
model_client = LLM(model=f"{openai_config.provider}/{openai_config.model}")


def get_model_client(response_format):
    """
    Get the model client.
    :return: The model client.
    """
    if response_format:
        return LLM(
            model=f"{openai_config.provider}/{openai_config.model}",
            response_format=response_format,
        )
    return model_client


