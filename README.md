# 🤖 Chatbot

Dự án Chatbot hỗ trợ trả lời tự động.

---

## 📦 Cấu hình môi trường

### 1. Tạo file `.env`

Tại thư mục /core của project, tạo file mới tên `.env` và thêm nội dung theo mẫu sau vào:

```env
PORT=
TOP_K_RETRIEVAL=

# Embedding
EMBEDDING_SERVICE=
EMBEDDING_MODEL_NAME=

# Qdrant
QDRANT_URL=
QDRANT_COLLECTION_NAME=

# Gemini
GEMINI_API_KEY=

# WikiJs
WIKI_JS_URL=

# LLM
LLM_URL_HOST=
LLM_MODEL_NAME=

STREAM_OUTPUT=

Tại thư mục /fe-streamlit của project, tạo file mới tên `.env` và thêm nội dung theo mẫu sau vào:
```env
BACKEND_API_URL=
