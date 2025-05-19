import os
from os.path import join
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)
from autogen_core.models import ModelFamily


# settings directory is the cwd dir with settings
settings_dir = join(
    os.getcwd(),
    "settings",
)

settings_file = join(settings_dir, "settings.toml")

# check if settings file exists, if not create it
# cp settings.example.toml settings.toml
if not os.path.exists(settings_file):
    print("Creating a new settings file from the example.")
    with open(settings_file, "w") as f:
        with open(join(settings_dir, "settings.example.toml"), "r") as example_file:
            f.write(example_file.read())


class ModelInfo(BaseModel):
    """True if the model supports vision, aka image input, otherwise False."""

    vision: bool = False
    """True if the model supports function calling, otherwise False."""
    function_calling: bool = False
    """True if the model supports json output, otherwise False. Note: this is different to structured json."""
    json_output: bool = False
    """Model family should be one of the constants from :py:class:`ModelFamily` or a string representing an unknown model family."""
    family: ModelFamily.ANY | str = ModelFamily.UNKNOWN


model_info = ModelInfo(
    vision=False,
    function_calling=True,
    json_output=False,
    family="unknown",
)


class OpenAISettings(BaseModel):
    api_key: str
    model: str = "gpt-4o"
    base_url: str = "https://api.openai.com/v1"
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    model_info: ModelInfo = model_info


class Settings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=settings_file)
    openai: OpenAISettings
    # any othere settings you want to add

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
    # Check if the settings directory exists
    if not os.path.exists(settings_dir):
        raise FileNotFoundError(f"Settings directory '{settings_dir}' does not exist.")

    settings = Settings()

    return settings


settings = init_settings()


openai_config = settings.openai

if openai_config is None:
    raise ValueError("OpenAI configuration not found in settings.")

if openai_config.api_key is None:
    raise ValueError("OpenAI API key not found in settings.")


# add openai env
os.environ["OPENAI_API_KEY"] = openai_config.api_key
os.environ["OPENAI_BASE_URL"] = openai_config.base_url
os.environ["MODEL"] = openai_config.model
