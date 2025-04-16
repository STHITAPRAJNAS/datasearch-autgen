
class UserProxyAgent:
    def __init__(
        self,
        planner_agent,
        confluence_agent,
        databricks_agent,
        graphql_agent,
        response_generator,
        state_manager,
    ):
        self.planner_agent = planner_agent
        self.confluence_agent = confluence_agent
        self.databricks_agent = databricks_agent
        self.graphql_agent = graphql_agent
        self.response_generator = response_generator
        self.state_manager = state_manager

    def _call_agent(self, agent, user_id, conversation_id, query):
      agent_name = type(agent).__name__
      method_name = f"query_{agent_name.lower().replace('agent', '')}"
      if hasattr(agent, method_name):
        result = getattr(agent, method_name)(query)
        self.state_manager.store_state(user_id, conversation_id, agent.__class__.__name__, result)
        return result
      return None

    def get_message(self, message: str, user_id: str, conversation_id: str):
        self.state_manager.add_message(user_id, conversation_id, {"sender": "user", "content": message, 'timestamp': 'now'})
        previous_messages = self.state_manager.get_messages(user_id, conversation_id)
        if previous_messages:
            plan = previous_messages + [{'sender': 'user', 'content': message, 'timestamp': 'now'}] + self.planner_agent.generate_plan(" ".join([m["content"] for m in previous_messages]) + message)
        else:
            plan = [{'sender': 'user', 'content': message, 'timestamp': 'now'}] + self.planner_agent.generate_plan(message)

        self.state_manager.add_message(user_id, conversation_id, {'sender': 'user', 'content': message, 'timestamp': 'now'})
        if isinstance(plan, str):
            return plan
        elif isinstance(plan, list):
            results = []
            for element in plan:
              result = self._call_agent(element, user_id, conversation_id, message)
              if result:
                results.append(result)
            if hasattr(self.response_generator, "generate_response"):
                response = self.response_generator.generate_response(results, message)
                self.state_manager.add_message(user_id, conversation_id, {'sender': 'response', 'content': response, 'timestamp': 'now'})
                return response
            else:
                self.state_manager.add_message(user_id, conversation_id, {'sender': 'response', 'content': " ".join([str(r) for r in results]), 'timestamp': 'now'})
                return results
        else:
            return str(plan)
