FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for Pillow/Graphics)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set Python path so 'src' is discoverable
ENV PYTHONPATH=/app

# Run app (Handles Render $PORT and HF 7860)
CMD sh -c "streamlit run src/app.py --server.port=${PORT:-7860} --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false"
