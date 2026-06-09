FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir torch==2.3.0 --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .

RUN pip install --no-cache-dir flask==3.0.3 transformers==4.41.2 prometheus-client==0.20.0 requests==2.32.3 pytest==8.2.2 selenium==4.21.0

COPY . .

RUN mkdir -p /app/logs

EXPOSE 5000

CMD ["python", "app.py"]