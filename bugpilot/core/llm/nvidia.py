from typing import List, Dict, Optional
from .base import BaseModel
import openai

class NvidiaModel(BaseModel):
    def __init__(self, api_key: Optional[str] = None, model_name: str = "meta/llama3-70b-instruct", **kwargs):
        super().__init__(api_key, model_name, **kwargs)
        if not self.api_key:
            raise ValueError("Nvidia API key is required")
        self.client = openai.OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )

    def generate(self, prompt: str, context: List[Dict[str, str]] = None) -> str:
        messages = context or []
        if prompt:
            messages.append({"role": "user", "content": prompt})
            
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.kwargs.get("temperature", 0.7),
                max_tokens=self.kwargs.get("max_tokens", 1024)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with Nvidia model: {str(e)}"
