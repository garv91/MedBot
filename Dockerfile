FROM python:3.10-slim-buster

WORKDIR /app

# Copy everything
COPY . /app

# Show what got copied
RUN echo "==> Listing contents of /app" && ls -la /app

# Show the actual content of requirements.txt
RUN echo "==> Printing requirements.txt" && cat /app/requirements.txt

# Install dependencies (fail if it fails)
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8080

CMD ["python3", "app.py"]
