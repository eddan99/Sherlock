from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    google_api_key: str
    upload_folder: str = "./uploads"
    embedding_model: str = "models/gemini-embedding-001"
    llm_model: str = "gemini-2.5-flash-lite"
    chroma_path: str = "./chroma_langchain_db"
    collection_name: str = "sherlock_collection"