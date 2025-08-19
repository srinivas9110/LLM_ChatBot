# test_inference.py
from __future__ import annotations
import os
from typing import List, Dict, Optional
from datetime import datetime
from huggingface_hub import InferenceClient

# Supported models for dropdown
SUPPORTED_MODELS = [
    "mistralai/Mistral-7B-Instruct-v0.2",   # Mistral 2.0
    "mistralai/Mistral-7B-Instruct-v0.3",   # Mistral 3.0
]

SYSTEM_PROMPT = (
    "You are a helpful, concise AI assistant. "
    "Answer clearly and use markdown when helpful."
)

class ChatBackend:
    def __init__(self, hf_token: Optional[str] = None, default_model: str = SUPPORTED_MODELS[0]):
        token = hf_token or os.getenv("HF_TOKEN")
        if not token:
            raise ValueError("No Hugging Face token found. Please set HF_TOKEN environment variable or pass it in.")
        self.client = InferenceClient(token=token)
        self.default_model = default_model

    def _now_iso(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def build_messages(self, user_input: str, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Return a new messages list with user input appended. Always includes a system prompt at the top."""
        msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
        msgs.extend(history)
        msgs.append({"role": "user", "content": user_input})
        return msgs

    def _format_prompt_fallback(self, messages: List[Dict[str, str]]) -> str:
        """Create a simple chat-style prompt for text-generation if chat API isn't available."""
        lines = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "system":
                lines.append(f"[SYSTEM] {content}\n")
            elif role == "user":
                lines.append(f"[USER] {content}\n")
            else:
                lines.append(f"[ASSISTANT] {content}\n")
        lines.append("[ASSISTANT] ")
        return "\n".join(lines)

    def chat(self, messages: List[Dict[str, str]], model: Optional[str] = None, max_tokens: int = 512) -> str:
        """Send a chat request. Tries chat endpoint; falls back to text-generation."""
        model_id = model or self.default_model
        try:
            # Try chat endpoint
            response = self.client.chat_completion(
                model=model_id,
                messages=messages,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to text-generation
            prompt = self._format_prompt_fallback(messages)
            response = self.client.text_generation(
                model=model_id,
                prompt=prompt,
                max_new_tokens=max_tokens,
            )
            return response.generated_text.strip()
