import os
from typing import List
from openai import OpenAI


class OpenAIClient:
    """OpenAI API client for chat completions."""
    def __init__(self, model: str = "gpt-4o-mini", request_timeout: int = 30):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.request_timeout = request_timeout
    def chat(self, messages: List[dict], max_tokens: int = 256, temperature: float = 0.0) -> str:
        """Send chat messages and return the assistant content."""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=self.request_timeout,
        )
        return resp.choices[0].message.content.strip()
    

