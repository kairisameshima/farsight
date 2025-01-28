import pinecone
from app.config import PINECONE_API_KEY, PINECONE_INDEX

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Access the index
index = pc.Index(PINECONE_INDEX)