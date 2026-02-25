FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for ChromaDB persistence
RUN mkdir -p /app/data/chromadb

# Ingest docs at build time (can also re-ingest at runtime via !ingest)
RUN python ingest.py || true

CMD ["python", "bot.py"]
