import boto3

class BedrockAgent:
    def __init__(self, bedrock_client, model_id, prompt):
        self.bedrock_client = bedrock_client
        self.model_id = model_id
        self.prompt = prompt

    def invoke(self, input):
        body = {"prompt": self.prompt + input,
                "max_tokens_to_sample": 500}

        response = self.bedrock_client.invoke_model(
            body=body, modelId=self.model_id
        )

        return response["body"].read().decode()