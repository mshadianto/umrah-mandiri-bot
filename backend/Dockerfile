FROM python:3.11-slim

WORKDIR /app

# Copy requirements from backend directory
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend directory
COPY backend ./

# Expose port
EXPOSE 8000

# Use shell form to expand PORT variable
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
