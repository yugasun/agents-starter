import os
from os.path import join
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

# TODO: make this dynamic
settings_dir = "/mnt/data/www/develop/agents-starter/settings"

settings_file = join(settings_dir, "settings.toml")


class OpenAISettings(BaseModel):
    api_key: str
    model: str = "gpt-4o"
    provider: str = "openai"
    base_url: str = "https://api.openai.com/v1"
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0


class SerperSettings(BaseModel):
    api_key: str
    base_url: str = "https://google.serper.dev/search"


class LangsmithSettings(BaseModel):
    tracing: str = "true"
    api_key: str
    endpoint: str = "https://api.langsmith.com/v1"
    project: str = "default"


class TavilySettings(BaseModel):
    api_key: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=settings_file)
    openai: OpenAISettings
    serper: SerperSettings

    # any othere settings you want to add
    langsmith: LangsmithSettings
    tavily: TavilySettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


def init_settings():
    """
    Initialize settings for the application.
    """
    # check if settings file exists, if not create it
    # cp settings.example.toml settings.toml
    if not os.path.exists(settings_file):
        print("Creating a new settings file from the example.")
        with open(settings_file, "w") as f:
            with open(join(settings_dir, "settings.example.toml"), "r") as example_file:
                f.write(example_file.read())

    # Check if the settings directory exists
    if not os.path.exists(settings_dir):
        raise FileNotFoundError(f"Settings directory '{settings_dir}' does not exist.")

    settings = Settings()

    openai_config = settings.openai

    if openai_config is None:
        raise ValueError("OpenAI configuration not found in settings.")

    if openai_config.api_key is None:
        raise ValueError("OpenAI API key not found in settings.")

    # add openai env
    os.environ["OPENAI_API_KEY"] = openai_config.api_key
    os.environ["OPENAI_BASE_URL"] = openai_config.base_url
    os.environ["MODEL"] = openai_config.model
    os.environ["SERPER_API_KEY"] = settings.serper.api_key
    os.environ["TAVILY_API_KEY"] = settings.tavily.api_key
    os.environ["LANGSMITH_TRACING"] = settings.langsmith.tracing
    os.environ["LANGSMITH_API_KEY"] = settings.langsmith.api_key
    os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith.endpoint
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith.project

    return settings


settings = init_settings()
