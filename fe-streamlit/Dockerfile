FROM python:3.11-slim

WORKDIR /app
COPY fe-streamlit /app
RUN pip install streamlit

# Nếu bạn có requirements.txt cho fe-streamlit thì:
COPY fe-streamlit/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fe-streamlit/.env ./
CMD ["streamlit", "run", "Hello.py", "--server.address=0.0.0.0", "--server.port=8501"]
