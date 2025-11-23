FROM python:3.11-slim

WORKDIR /app

# Copy backend files
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

# Change to backend directory
WORKDIR /app/backend

# Use shell form to expand PORT variable properly
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
