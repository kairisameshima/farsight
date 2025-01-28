from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# PostgreSQL settings
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
POSTGRES_USER = os.getenv("POSTGRES")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Pinecone settings
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")