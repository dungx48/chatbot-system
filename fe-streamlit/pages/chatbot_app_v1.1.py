import os
import json
import time
import logging
import threading
from typing import Generator

import httpx
import streamlit as st
from dotenv import load_dotenv

# -----------------------------------------------------------------------
# Cấu hình Logging
# -----------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------
# Đọc biến môi trường
# -----------------------------------------------------------------------
load_dotenv()
BACKEND_API_URL_V1_1 = os.getenv("BACKEND_API_URL_V1_1")

# -----------------------------------------------------------------------
# HTTP client để stream token
# -----------------------------------------------------------------------
class ChatClient:
    """HTTP client cho streaming chat responses token-by-token."""
    def __init__(self, url: str):
        self.url = url

    def stream_chat(self, question: str) -> Generator[str, None, None]:
        with httpx.stream("POST", self.url,
                          json={"question": question, "user_prompt": ""},
                          timeout=None) as resp:
            resp.raise_for_status()
            for raw in resp.iter_lines():
                if not raw:
                    continue
                text = raw.decode("utf-8", errors="ignore") if isinstance(raw, (bytes, bytearray)) else raw
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    logger.debug("Không parse được JSON: %s", text)
                    continue

                if data.get("meta") is not None:
                    continue
                if token := data.get("token"):
                    yield token
                    continue
                if choices := data.get("choices"):
                    delta = choices[0].get("delta", {}).get("content")
                    if delta:
                        yield delta

# -----------------------------------------------------------------------
# CSS tùy chỉnh cho chat bubbles
# -----------------------------------------------------------------------
def inject_css() -> None:
    st.markdown(
        """
        <style>
          p { line-height: 1.2 !important; margin: 0 !important; }
          .streamlit-expanderHeader, .streamlit-expanderContent {
            padding: 0.25rem 0.5rem !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------
# Thread chỉ cập nhật biến elapsed_container["time"]
# -----------------------------------------------------------------------
def update_timer(start_time: float, stop_event: threading.Event, elapsed_container: dict):
    while not stop_event.is_set():
        elapsed_container["time"] = time.time() - start_time
        time.sleep(0.1)

# -----------------------------------------------------------------------
# Hiển thị lịch sử chat
# -----------------------------------------------------------------------
def render_history(messages: list[dict[str, str]]) -> None:
    for msg in messages:
        role = "user" if msg["role"] == "user" else "assistant"
        st.chat_message(role).write(msg["content"])

# -----------------------------------------------------------------------
# Hàm chính
# -----------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title="Chatbot Chotbat",
        page_icon="🤖",
        layout="wide"
    )
    st.title("🤖 Chatbot Chotbat")

    inject_css()

    # Khởi tạo session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Xin chào! Tôi có thể giúp gì?"}
        ]

    # Hiển thị lịch sử chat
    render_history(st.session_state.messages)

    client = ChatClient(BACKEND_API_URL_V1_1)

    # Xử lý prompt mới
    if prompt := st.chat_input("Hỏi bất kỳ điều gì:"):
        # Lưu và show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Chuẩn bị đo thời gian
        start_time = time.time()
        stop_event = threading.Event()
        elapsed_container = {"time": 0.0}

        # Placeholder cho UI
        timer_ph  = st.empty()
        think_ph  = st.empty()
        answer_ph = st.empty()

        # Khởi thread tính elapsed
        timer_thread = threading.Thread(
            target=update_timer,
            args=(start_time, stop_event, elapsed_container),
            daemon=True
        )
        timer_thread.start()

        # --- Tất cả UI của assistant nằm trong khối này ---
        with st.chat_message("assistant"):
            in_think = True
            think_buf = ""
            answer_buf = ""

            for token in client.stream_chat(prompt):
                # Cập nhật thời gian chờ
                elapsed = elapsed_container["time"]
                timer_ph.info(f"⏳ Đang suy nghĩ… {elapsed:.1f}s")

                if in_think:
                    think_buf += token
                    think_ph.info(think_buf)
                    if "</think>" in think_buf:
                        think_ph.empty()
                        timer_ph.info(f"✅ Đã suy nghĩ xong sau {elapsed:.2f}s")
                        _, after = think_buf.split("</think>", 1)
                        answer_buf += after
                        answer_ph.write(answer_buf)
                        in_think = False
                else:
                    answer_buf += token
                    answer_ph.write(answer_buf)

            # Nếu không thấy tag </think>
            if in_think:
                think_ph.empty()
                elapsed = elapsed_container["time"]
                timer_ph.success(f"🤔 Đã suy nghĩ trong {elapsed:.2f}s")
                answer_ph.write(answer_buf)

            # Dừng thread tính thời gian và chờ kết thúc
            stop_event.set()
            timer_thread.join()

            # Hiển thị tổng thời gian trả lời
            total = elapsed_container["time"]
            timer_ph.success(f"✅ Thời gian trả lời: {total:.2f}s")
        # --- Kết thúc khối assistant ---

        # Lưu lại vào history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_buf
        })

if __name__ == "__main__":
    main()
