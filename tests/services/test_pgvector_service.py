import pytest
from src.services.pgvector_service import PGVectorService

@pytest.fixture
def pgvector_service():
    return PGVectorService()


def test_create_embedding(pgvector_service):
    embedding = pgvector_service.create_embedding("test")
    assert isinstance(embedding, list), "create_embedding should return a list"
    assert all(
        isinstance(x, float) for x in embedding
    ), "All elements in the list should be floats"


def test_query_vector_db(pgvector_service):
    results = pgvector_service.query_vector_db([0.1, 0.2])
    assert isinstance(results, list), "query_vector_db should return a list"
    assert all(isinstance(x, str) for x in results), "All elements in the list should be strings"