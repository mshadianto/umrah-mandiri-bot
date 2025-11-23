#!/bin/bash
echo "Starting Umrah Assistant..."

# Kill old processes
pkill -9 python
sleep 2

# Start backend in background
cd backend
uvicorn app.main:app --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "Waiting for backend..."
sleep 10

# Check backend
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend is running!"
else
    echo "❌ Backend failed to start!"
    exit 1
fi

# Start bot
cd ../telegram-bot
python bot.py

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
