from google.adk.models.lite_llm import LiteLlm


from ..settings import openai_config


model_client = LiteLlm(
    model=f"{openai_config.provider}/{openai_config.model}",
    api_key=openai_config.api_key,
    api_base=openai_config.base_url,
)
