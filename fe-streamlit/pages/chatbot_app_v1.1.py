import os
import json
import time
import logging
from typing import Generator, Union

import httpx
import streamlit as st
from dotenv import load_dotenv

# ------------------------------------------------------------------------------
# Setup logging
# ------------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Configuration & Client
# ------------------------------------------------------------------------------
load_dotenv()
BACKEND_API_URL_V1_1 = os.getenv("BACKEND_API_URL_V1_1")

class ChatClient:
    """HTTP client for streaming chat responses token-by-token."""
    def __init__(self, url: str):
        self.url = url

    def stream_chat(self, question: str) -> Generator[str, None, None]:
        """
        Gửi request và yield từng token khi backend trả về.
        Backend phải trả về JSON lines với key "token" hoặc OpenAI style.
        """
        with httpx.stream("POST", self.url,
                          json={"question": question, "user_prompt": ""},
                          timeout=None) as resp:
            resp.raise_for_status()
            for raw in resp.iter_lines():
                if not raw:
                    continue
                text = raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    logger.debug("Không parse được JSON: %s", text)
                    continue

                # skip metadata
                if data.get("meta") is not None:
                    continue

                # token-based streaming
                if token := data.get("token"):
                    yield token
                    continue

                # OpenAI-style
                choices = data.get("choices")
                if choices:
                    delta = choices[0].get("delta", {}).get("content")
                    if delta:
                        yield delta

# ------------------------------------------------------------------------------
# UI Helpers
# ------------------------------------------------------------------------------
def inject_css() -> None:
    """Giảm line-height & padding cho chat bubbles."""
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

def render_history(messages: list[dict[str,str]]) -> None:
    """In ra toàn bộ history chat bubbles."""
    for msg in messages:
        role = "user" if msg["role"] == "user" else "assistant"
        st.chat_message(role).write(msg["content"])

def main() -> None:
    st.set_page_config(page_title="Chatbot Chotbat", page_icon="🤖", layout="wide")
    st.title("🤖 Chatbot Chotbat")

    inject_css()

    # Khởi tạo session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role":"assistant","content":"Xin chào! Tôi có thể giúp gì?"}]

    render_history(st.session_state.messages)
    client = ChatClient(BACKEND_API_URL_V1_1)

    # Xử lý prompt mới
    if prompt := st.chat_input("Bạn:"):
        st.session_state.messages.append({"role":"user","content":prompt})
        st.chat_message("user").write(prompt)

        # Streaming response
        start = time.time()
        with st.chat_message("assistant"):
            timer_ph = st.empty()
            think_ph = st.empty()     # để hiển thị <think>…</think>
            answer_ph = st.empty()    # để hiển thị phần answer

            in_think = True           # cờ đang ở giai đoạn think
            think_buf = ""
            answer_buf = ""


            for token in client.stream_chat(prompt):
                if in_think:
                    think_buf += token
                    # nếu phát hiện kết thúc <think>
                    if "</think>" in think_buf:
                        # đo thời gian suy nghĩ
                        total_think = time.time() - start
                        # xoá hoàn toàn vùng think
                        think_ph.empty()
                        # hiển thị thông báo đã suy nghĩ x giây
                        timer_ph.info(f"✅ Đã suy nghĩ xong sau {total_think:.2f}s")
                        # phần dư sau </think> là bắt đầu của answer
                        _, after = think_buf.split("</think>", 1)
                        answer_buf += after
                        answer_ph.write(answer_buf)
                        in_think = False
                    else:
                        # vẫn đang suy nghĩ, show nội dung trong think
                        think_ph.info(think_buf)
                        # cập nhật thời gian chờ
                        elapsed = time.time() - start
                        timer_ph.info(f"⏳ Đang suy nghĩ… {elapsed:.1f}s")
                        elapsed = time.time() - start
                        timer_ph.info(f"⏳ Đang xử lý… {elapsed:.1f}s")
                else:
                    # giai đoạn hiển thị answer
                    answer_buf += token
                    answer_ph.write(answer_buf)

            # nếu user stream không có <think> tag, vẫn hiện timer ở đây
            if in_think:
                total_think = time.time() - start
                think_ph.empty()
                timer_ph.success(f"🤔 Đã suy nghĩ trong {total_think:.2f}s")

        # Lưu vào history
        st.session_state.messages.append({"role":"assistant","content":timer_ph})

if __name__ == "__main__":
    main()
