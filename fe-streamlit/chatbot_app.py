import streamlit as st
import requests

st.set_page_config(page_title="Chatbot Demo", page_icon="🤖", layout="wide")
st.title("🤖 Chatbot Demo")
st.write("Giao diện chat đơn giản với Streamlit!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Xin chào! Tôi có thể giúp gì cho bạn?"}
    ]

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    align = "user" if msg["role"] == "user" else "assistant"
    st.chat_message(align).write(msg["content"])

if prompt := st.chat_input("Nhập câu hỏi..."):
    # 1. Hiện câu hỏi ngay
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Hiệu ứng loading trong lúc gọi API
    with st.spinner("🤖 Đang suy nghĩ..."):
        try:
            res = requests.post(
                "http://localhost:8000/v1/chat",
                json={
                    "user_prompt": "Là một nhân viên ngân hàng, tôi sẽ tư vấn cho khách",
                    "question": prompt,
                },
                timeout=150,
            )
            data = res.json()
            answer = data.get("answer", "Không nhận được phản hồi từ bot.")
        except Exception as e:
            answer = f"Lỗi: {e}"

        st.session_state.messages.append({"role": "bot", "content": answer})
    st.rerun()