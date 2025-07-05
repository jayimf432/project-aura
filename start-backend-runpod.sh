#!/bin/bash
echo "🚀 Starting Project Aura Backend on RunPod..."

# Get port from environment or use default
PORT=${RUNPOD_PORT:-8000}

cd backend
source venv/bin/activate

# Set environment variables for production
export ENVIRONMENT=production
export DEBUG=false
export HOST=0.0.0.0
export PORT=$PORT

echo "Starting backend on port $PORT..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
