from langchain.chat_models import init_chat_model

from ..settings import openai_config


# Define a model client. You can use other model client that implements
# the `ChatCompletionClient` interface.
model_client = init_chat_model(model=f"{openai_config.provider}:{openai_config.model}")


def get_model_client(response_format):
    """
    Get the model client.
    :return: The model client.
    """
    if response_format:
        return init_chat_model(
            model=f"{openai_config.provider}/{openai_config.model}",
            response_format=response_format,
        )
    return model_client
