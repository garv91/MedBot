FROM python:3.10-slim-bookworm

WORKDIR /app

COPY . /app

RUN ls -la /app && cat requirements.txt && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python3", "app.py"]
