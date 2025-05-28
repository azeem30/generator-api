import requests
import json

class MistralClient:
    def __init__(self, base_url, api_key, model_name):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_qa(self, context, qa_count, options=None):
        """Generate descriptive questions and answers on the context according to the specified options"""
        # Preparation of prompt
        prompt = f"Generate {qa_count} large descriptive questions and answers based on the following context without any formatting: {context}. Only return the Questions and Answers as a response in a JSON parsable string. The string should be an array consisting of JSON objects with keys 'Q' and 'A'. Do not add any heading, title or footing to the response."
        if options:
            pass

        payload = {
            "model": self.model_name,
            "messages": [ { "role": "user", "content": prompt } ],
        }

        # Send request the model API
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers = self.headers,
                data = json.dumps(payload)
            )
            response.raise_for_status()
            response_data = response.json()["choices"][0]
            response = response_data["message"]["content"]
            
            # Return the generated response
            if response:
                return response
            return { "message": "Failed to generate questions and answers." }
        except Exception as e:
            return { "error": str(e) }
