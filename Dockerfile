# Use a modern, supported Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the Flask default port
EXPOSE 8080

# Run the application
CMD ["python3", "app.py"]
