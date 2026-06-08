# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into container
COPY . .

# Create logs directory (needed by app.py for writing predictions)
RUN mkdir -p /app/logs

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]