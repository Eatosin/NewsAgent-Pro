FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]
