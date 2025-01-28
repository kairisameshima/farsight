import pinecone
from app.config import PINECONE_API_KEY, PINECONE_INDEX
from app.services.openai_service import get_query_embedding
# Initialize Pinecone
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Access the index
index = pc.Index(PINECONE_INDEX)

def query_pinecone(query_text, filters=None):
    # Convert the query text to a vector
    query_embedding = get_query_embedding(query_text)
    print(len(query_embedding.data[0].embedding))


    return index.query(
        vector=query_embedding.data[0].embedding,
        top_k=10,
        include_metadata=True,
        filter=filters
    )
