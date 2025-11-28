import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env from backend folder if present so os.getenv() picks values during local runs
_env_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(_env_path):
    load_dotenv(_env_path)

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/internshipdb")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    JOBSCRAPER_RATE_LIMIT: float = float(os.getenv("JOBSCRAPER_RATE_LIMIT", "1.0"))

settings = Settings()
