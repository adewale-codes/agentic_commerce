from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    app_name: str = "agentic-commerce-backend"
    data_path: str = os.getenv("PRODUCTS_JSON_PATH", "data/products.json")
    max_search_results: int = int(os.getenv("MAX_SEARCH_RESULTS", "50"))

settings = Settings()
