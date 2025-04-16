import pytest
from src.services.graphql_service import GraphqlService

@pytest.fixture
def graphql_service():
    return GraphqlService()


def test_execute_graphql_query(graphql_service):
    
    result = graphql_service.execute_graphql_query("some query")
    assert isinstance(result, str)

