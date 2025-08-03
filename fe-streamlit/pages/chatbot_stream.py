# streamlit_app.py
import streamlit as st
import httpx
import json

st.set_page_config(
    page_title="Chatbot Realtime",
    page_icon="🤖",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Xin chào! Tôi có thể giúp gì?"}
    ]

def chat_stream(question: str):
    req_body = {
        "question": question,
        "user_prompt": question
    }
    # Thay URL cho đúng endpoint của bạn
    with httpx.stream(
        "POST",
        "http://localhost:8000/chat/v1_1",
        json=req_body,
        timeout=1200
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            # bỏ qua dòng rỗng
            if not line:
                continue

            # nếu là bytes thì decode
            text = line.decode('utf-8') if isinstance(line, (bytes, bytearray)) else line

            # parse JSON, skip nếu lỗi
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                continue

            # lấy token, bỏ qua nếu không có
            token = data.get("token")
            if token:
                yield token

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input
if prompt := st.chat_input("Bạn:"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    assistant_msg = st.chat_message("assistant")
    full_resp = ""

    # Stream từng token
    for chunk in chat_stream(prompt):
        assistant_msg.write(chunk, end="")
        full_resp += chunk

    # Lưu lại message đầy đủ
    st.session_state.messages.append({"role": "assistant", "content": full_resp})
