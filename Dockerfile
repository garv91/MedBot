FROM python:3.10-buster

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y gcc build-essential && \
    python3 -m ensurepip && \
    python3 -m pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "==> requirements.txt" && cat requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python3", "app.py"]
