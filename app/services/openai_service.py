from openai import OpenAI
from app.config import OPENAI_API_KEY

# Initialize OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def get_query_embedding(query_text):
    # Convert the query text to a vector
    query_embedding = client.embeddings.create(
        model="text-embedding-3-large",
        input=query_text,
    )

    return query_embedding