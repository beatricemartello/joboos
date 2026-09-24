from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "JOBOS"
    database_url: str = "sqlite:////data/jobos.db"
    openai_api_key: str = ""
    target_roles: str = ""
    target_locations: str = ""
    excluded_countries: str = ""
    min_match_score: int = 75
    min_salary: str = ""
    relocation: bool = True
    sponsorship: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def csv(self, value: str):
        return [x.strip() for x in value.split(",") if x.strip()]

settings = Settings()
