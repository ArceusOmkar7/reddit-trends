from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Reddit Trends API"
    app_version: str = "0.1.0"

    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "reddit-trends/0.1"

    poll_interval_seconds: int = 300
    database_url: str = "sqlite:///./data.db"
    enable_ingestion: bool = False
    subreddits: str = "worldnews,india,technology,artificial,business,politics,science,movies"
    keywords: str = "elections,ai releases,geopolitical conflicts,inflation,layoffs,climate,entertainment"

    class Config:
        env_file = ".env"


settings = Settings()
