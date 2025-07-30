FROM python:3.11-slim-bookworm

# Set timezone to Vietnam
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install additional system dependencies for Python libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uv (Python package manager)
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
# Add uv to PATH
ENV PATH="/root/.local/bin/:$PATH"


# Copy source code
WORKDIR /app
COPY ../core /app/core
COPY ../core/requirements.txt /app/requirements.txt

# Sync the project into a new environment, using the frozen lockfile
RUN uv pip install --system -r requirements.txt

# Presuming there is a `my_app` command provided by the project
WORKDIR /app/core
CMD ["python", "main.py"]