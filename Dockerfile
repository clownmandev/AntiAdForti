FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir requests

COPY fetch_domains.py .

RUN echo 'python3 -m http.server 8080' > start.sh && chmod +x start.sh

CMD ["sh", "-c", "while true; do python3 fetch_domains.py; sleep 86400; done & ./start.sh"]
