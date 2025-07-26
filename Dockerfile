FROM python:3.10-slim-buster

# Install pip, basic tools, and dependencies safely
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libffi-dev \
    libssl-dev \
    && python3 -m ensurepip \
    && python3 -m pip install --upgrade pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set workdir and copy files
WORKDIR /app
COPY . /app

# Print requirements and install them
RUN echo "==> requirements.txt" && cat requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Expose port for Flask
EXPOSE 8080

CMD ["python3", "app.py"]
