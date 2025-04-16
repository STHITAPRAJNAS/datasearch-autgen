class StateManager:
    def __init__(self):
        self.state = {}  # {user_id: {conversation_id: {agent_name: state_data, "messages": []}}}

    def store_state(self, user_id, conversation_id, agent_name, state_data):
        if user_id not in self.state:
            self.state[user_id] = {}
        if conversation_id not in self.state[user_id]:
            self.state[user_id][conversation_id] = {}
        self.state[user_id][conversation_id][agent_name] = state_data

    def get_state(self, user_id, conversation_id, agent_name):
        if user_id in self.state and conversation_id in self.state[user_id]:
            return self.state[user_id][conversation_id].get(agent_name)
        return None

    def clear_state(self, user_id, conversation_id, agent_name=None):
        if user_id in self.state and conversation_id in self.state[user_id]:
            if agent_name:
                if agent_name in self.state[user_id][conversation_id]:
                    del self.state[user_id][conversation_id][agent_name]
            else:
                del self.state[user_id][conversation_id]

    def add_message(self, user_id, conversation_id, message):
        if user_id not in self.state:
            self.state[user_id] = {}
        if conversation_id not in self.state[user_id]:
            self.state[user_id][conversation_id] = {}
        if "messages" not in self.state[user_id][conversation_id]:
          self.state[user_id][conversation_id]["messages"]=[]
        self.state[user_id][conversation_id]["messages"].append(message)

    def get_messages(self, user_id, conversation_id):
        return self.state.get(user_id, {}).get(conversation_id, {}).get("messages", [])