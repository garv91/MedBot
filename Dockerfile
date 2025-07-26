FROM python:3.10-slim-buster

# Avoid pip-related problems
RUN apt-get update && apt-get install -y gcc build-essential && \
    python3 -m ensurepip && python3 -m pip install --upgrade pip

WORKDIR /app
COPY . /app

# Show contents of requirements.txt
RUN echo "==> requirements.txt" && cat requirements.txt

# Explicit pip install
RUN python3 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python3", "app.py"]
