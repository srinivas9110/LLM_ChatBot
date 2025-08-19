# app.py
from __future__ import annotations
import os
from datetime import datetime
from typing import List, Dict

import streamlit as st
from huggingface_hub import InferenceClient

# -----------------------------
# Supported Models
# -----------------------------
SUPPORTED_MODELS = {
    "Mistral 7B Instruct v0.2": "mistralai/Mistral-7B-Instruct-v0.2",
    "Llama 3 8B Instruct": "meta-llama/Meta-Llama-3-8B-Instruct",
    "Falcon 7B Instruct": "tiiuae/falcon-7b-instruct",
}

# -----------------------------
# Backend Wrapper
# -----------------------------
class ChatBackend:
    def __init__(self, model: str, token: str):
        self.client = InferenceClient(model=model, token=token)

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        messages format: [{"role": "user", "content": "Hi"}]
        """
        response = self.client.chat_completion(
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
            max_tokens=512,
            temperature=0.7,
        )
        return response.choices[0].message["content"]

# -----------------------------
# Page Config & Simple Theme
# -----------------------------
st.set_page_config(page_title="🧠 LLM Playground", page_icon="🤖", layout="centered")

# Session state initialization
st.session_state.setdefault("theme", "Dark")
st.session_state.setdefault("messages", [])

def apply_theme(theme: str):
    if theme == "Dark":
        st.markdown(
            """
            <style>
            body, .stApp { background: #0f1115 !important; color: #e5e7eb !important; }
            .stTextInput input, .stTextArea textarea { background: #111827 !important; color: #e5e7eb !important; }
            .stSelectbox div[data-baseweb="select"] > div { background: #111827 !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )

apply_theme(st.session_state.theme)

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.title("🧠 LLM Playground")
model_choice = st.sidebar.selectbox("Model", options=list(SUPPORTED_MODELS.keys()), index=0)

# Token retrieval order: st.secrets -> env -> input
hf_token = None
if hasattr(st, "secrets"):
    hf_token = st.secrets.get("HF_TOKEN")
hf_token = hf_token or os.getenv("HF_TOKEN")
if not hf_token:
    hf_token = st.sidebar.text_input(
        "Hugging Face Token", 
        type="password", 
        help="Stored only in memory for this session."
    )

st.sidebar.divider()
st.session_state.theme = st.sidebar.radio(
    "Theme", ["Light", "Dark"], 
    index=(1 if st.session_state.theme == "Dark" else 0)
)
apply_theme(st.session_state.theme)

# Export and Clear
col_a, col_b = st.sidebar.columns(2)
with col_a:
    clear = st.button("🧹 Clear Chat")
with col_b:
    export_click = st.button("⬇️ Export .txt")

# -----------------------------
# Clear Chat Logic
# -----------------------------
if clear:
    st.session_state.messages.clear()

# -----------------------------
# Export Chat Logic
# -----------------------------
if export_click and st.session_state.messages:
    filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for msg in st.session_state.messages:
            f.write(f"{msg['role'].upper()}: {msg['content']}\n\n")
    st.sidebar.success(f"Exported as {filename}")

# -----------------------------
# Main Chat UI
# -----------------------------
st.title("🧠 LLM Playground")
st.write("Chat with different Hugging Face models!")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# Input box
if prompt := st.chat_input("Type your message..."):
    if not hf_token:
        st.warning("Please provide a Hugging Face API token in the sidebar.")
    else:
        # Append user msg
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        # Query model
        backend = ChatBackend(SUPPORTED_MODELS[model_choice], hf_token)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = backend.chat(st.session_state.messages)
                st.markdown(response)

        # Save response
        st.session_state.messages.append({"role": "assistant", "content": response})
