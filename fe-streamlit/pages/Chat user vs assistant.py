import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.orchestrator.service import RAGService
from core.models.request.chat_request import ChatRequest

import streamlit as st

print('\n'.join(sys.path))

st.markdown("""
    ### Demo
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for item in st.session_state.messages:
    role = item["role"]
    content = item["content"]
    with st.chat_message(role):
        st.markdown(content)
prompt = st.chat_input("Say something")

svc = RAGService()
if prompt:
    req = ChatRequest(
        user_prompt="Với tư cách là chuyên viên ngân hàng, hãy trả lời câu hỏi của người dùng.",
        question=prompt
    )
    bot_msg = svc.chat(req)["answer"]
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_msg
    })
        