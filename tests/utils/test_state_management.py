import pytest
from src.utils.state_management import StateManager

@pytest.fixture
def state_manager():
    return StateManager()

def test_store_data(state_manager):
    user_id = "test_user"
    conversation_id = "test_conv"
    agent_name = "test_agent"
    data = {"test_key": "test_value"}
    state_manager.store_state(user_id, conversation_id, agent_name, data)
    retrieved_data = state_manager.get_state(user_id, conversation_id, agent_name)
    assert retrieved_data == data

def test_retrieve_data(state_manager):
    user_id = "test_user"
    conversation_id = "test_conv"
    agent_name = "test_agent"
    data = {"test_key": "test_value"}
    state_manager.store_state(user_id, conversation_id, agent_name, data)
    retrieved_data = state_manager.get_state(user_id, conversation_id, agent_name)
    assert retrieved_data == data

def test_add_message(state_manager):
    user_id = "test_user"
    conversation_id = "test_conv"
    message = {"sender": "test_sender", "content": "test_content"}
    state_manager.add_message(user_id, conversation_id, message)
    messages = state_manager.get_messages(user_id, conversation_id)
    assert message in messages

def test_get_messages(state_manager):
    user_id = "test_user"
    conversation_id = "test_conv"
    messages = [
        {"sender": "test_sender1", "content": "test_content1"},
        {"sender": "test_sender2", "content": "test_content2"}
    ]
    for message in messages:
        state_manager.add_message(user_id, conversation_id, message)
    retrieved_messages = state_manager.get_messages(user_id, conversation_id)
    assert len(retrieved_messages) == len(messages)
    assert all(message in retrieved_messages for message in messages)

def test_clear_data(state_manager):
    user_id = "test_user"
    conversation_id = "test_conv"
    agent_name = "test_agent"
    data = {"test_key": "test_value"}
    state_manager.store_state(user_id, conversation_id, agent_name, data)
    state_manager.clear_state(user_id, conversation_id,agent_name)
    retrieved_data = state_manager.get_state(user_id, conversation_id, agent_name)
    assert retrieved_data == {}

def test_clear_conversation(state_manager):
    user_id = "test_user"
    conversation_id = "test_conv"
    agent_name = "test_agent"
    data = {"test_key": "test_value"}
    message = {"sender": "test_sender", "content": "test_content"}
    state_manager.store_state(user_id, conversation_id, agent_name, data)
    state_manager.add_message(user_id, conversation_id, message)
    state_manager.clear_state(user_id, conversation_id)
    retrieved_data = state_manager.get_state(user_id, conversation_id, agent_name)
    messages = state_manager.get_messages(user_id, conversation_id)
    assert retrieved_data == {}
    assert len(messages) == 0