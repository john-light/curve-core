from pathlib import Path

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(BASE_DIR, "settings", "env"))

    DEBUG: bool = True  # TODO: set to False when ready
    DEV: bool = False

    WEB3_PROVIDER_URL: str


settings = Settings()


def get_chain_settings(chain: str):
    config_file = Path(BASE_DIR, "settings", "chains", f"{chain}.yaml")

    class ChainConfig(BaseSettings):
        model_config = SettingsConfigDict(yaml_file=config_file)

        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            sources = super().settings_customise_sources(
                settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings
            )
            return YamlConfigSettingsSource(settings_cls, yaml_file=config_file), *sources

        # chain settings from config file
        chain: str
        chain_id: int

        weth: str
        owner: str
        fee_receiver: str

    return ChainConfig()
