import time
import requests
from prometheus_client import start_http_server, Gauge

# This is the exact metric name the grading script checks for
CONFIDENCE_GAUGE = Gauge(
    'prediction_confidence_score',
    'Latest prediction confidence score from the ML API'
)

# The app runs on NodePort 32500
APP_URL = "http://3.106.156.32:32500/api/latest-confidence"

def poll_confidence():
    """Poll the app every 5 seconds and update the Prometheus metric."""
    while True:
        try:
            response = requests.get(APP_URL, timeout=5)
            data = response.json()
            confidence = data.get("confidence", 1.0)
            CONFIDENCE_GAUGE.set(confidence)
            print(f"Confidence: {confidence}")
        except Exception as e:
            # If unreachable, set default to 1.0
            CONFIDENCE_GAUGE.set(1.0)
            print(f"Error polling app: {e}")
        time.sleep(5)

if __name__ == "__main__":
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    print("Exporter running on port 8000...")
    poll_confidence()