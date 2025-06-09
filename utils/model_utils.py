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

    def generate_qa(self, context, qa_pairs_array):
        """Generate descriptive questions and answers on the context according to the specified options"""
        # Preparation of prompt
        begin_prompt = """
            Generate large descriptive questions and answers for the following context:\n
        """

        middle_prompt = f"""
            The context is {context}.\n
        """

        pairs_prompt = ""
        for i, qa_pairs in enumerate(qa_pairs_array):
            pairs_prompt += f"For File {i + 1}, Generate ${qa_pairs} Q&A pairs.\n"

        end_prompt = f"""
            Do not generate the title of json.
            The Generated result should not contain any headers, footers, anything that is not required.
            The result of the prompt should only be a JSON parsable array where each object contains the keys 'Q' and 'A'.
        """

        prompt = begin_prompt + middle_prompt + pairs_prompt + end_prompt

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
                if response[3:7] == "json":
                    last_index = len(response) - 1
                    response = response[7:last_index - 2]
                return response
            return { "message": "Failed to generate questions and answers." }
        except Exception as e:
            return { "error": str(e) }
