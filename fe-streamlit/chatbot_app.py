import os
import requests
import streamlit as st
from dotenv import load_dotenv
import time
import threading

load_dotenv(dotenv_path=".env")
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/v1/chat")

st.set_page_config(page_title="Chatbot Demo", page_icon="🤖", layout="wide")
st.title("🤖 Chatbot Demo")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Xin chào! Tôi có thể giúp gì cho bạn?"}
    ]

for msg in st.session_state.messages:
    align = "user" if msg["role"] == "user" else "assistant"
    st.chat_message(align).write(msg["content"])

def call_api(prompt, result_container):
    try:
        res = requests.post(
            BACKEND_API_URL,
            json={
                "user_prompt": "",
                "question": prompt,
            },
            timeout=150,
        )
        data = res.json()
        answer = data.get("answer", "Không nhận được phản hồi từ bot.")
    except Exception as e:
        answer = f"Lỗi: {e}"
    result_container["answer"] = answer

if prompt := st.chat_input("Nhập câu hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Chuẩn bị biến chia sẻ kết quả cho thread
    result_container = {"answer": None}

    # Tạo và chạy thread API
    thread = threading.Thread(target=call_api, args=(prompt, result_container))
    thread.start()

    # Hiển thị timer realtime
    timer_placeholder = st.empty()
    start_time = time.time()
    while thread.is_alive():
        elapsed = time.time() - start_time
        timer_placeholder.info(f"⏳ Đang suy nghĩ... {elapsed:.1f} giây")
        time.sleep(0.1)  # Cập nhật mỗi 0.1s

    thread.join()
    elapsed = time.time() - start_time
    timer_placeholder.success(f"✅ Thời gian trả lời: {elapsed:.2f} giây")
    
    # Hiển thị kết quả
    answer = result_container["answer"] + f"\n\n⏱️ Thời gian phản hồi: {elapsed:.2f} giây"
    st.session_state.messages.append({"role": "bot", "content": answer})

    st.rerun()
