import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-pro"
    
    # Vector Store Configuration
    CHROMA_PERSIST_DIRECTORY = "./chroma_db"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # RAG Configuration
    TOP_K_RESULTS = 5
    SIMILARITY_THRESHOLD = 0.7
    
    # Mock Data Configuration
    MOCK_DATA_DIR = "./mock_data"
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
