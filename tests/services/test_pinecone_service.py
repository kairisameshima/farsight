from app.services.pinecone_service import index

def test_pinecone_service():
    assert index is not None
    assert index.describe_index_stats().dimension == 3072