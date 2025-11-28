import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Prefer an explicit backend/.env located next to this file's package root.
# This lets the backend pick values reliably regardless of current working directory.
_here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/app -> backend
_env_path_backend = os.path.join(_here, ".env")
_env_path_cwd = os.path.join(os.getcwd(), ".env")
if os.path.exists(_env_path_backend):
    load_dotenv(_env_path_backend)
elif os.path.exists(_env_path_cwd):
    load_dotenv(_env_path_cwd)


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/internshipdb")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    JOBSCRAPER_RATE_LIMIT: float = float(os.getenv("JOBSCRAPER_RATE_LIMIT", "1.0"))
    # Allow running dev-only seed endpoints via API when True (default False)
    ALLOW_DEV_SEED: bool = bool(os.getenv("ALLOW_DEV_SEED", "False") in ("True", "true", "1"))


settings = Settings()
